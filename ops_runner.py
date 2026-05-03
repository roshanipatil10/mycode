"""
ops_runner.py — Daily Operations Runner
Flask web app for day-to-day DevOps tasks.
Compatible: Python 3.6 | Flask 2.0.3 | RHEL 7.9
"""

import os
import subprocess
import tempfile
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def run_command(cmd_list, timeout=60):
    """Run a command list safely via subprocess (no shell=True).
    Returns (stdout, stderr, returncode)."""
    try:
        proc = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(timeout=timeout)
        return (
            stdout.decode("utf-8", errors="replace"),
            stderr.decode("utf-8", errors="replace"),
            proc.returncode
        )
    except subprocess.TimeoutExpired:
        proc.kill()
        return "", "Command timed out.", 1
    except FileNotFoundError:
        return "", "Command not found: {}".format(cmd_list[0]), 1


def list_directory(dir_path):
    """Return formatted directory listing using os.listdir.
    Raises ValueError or PermissionError on bad/inaccessible path."""
    if not os.path.exists(dir_path):
        raise ValueError("Path does not exist: {}".format(dir_path))
    if not os.path.isdir(dir_path):
        raise ValueError("Not a directory: {}".format(dir_path))

    entries = []
    for name in sorted(os.listdir(dir_path)):
        full = os.path.join(dir_path, name)
        kind = "DIR " if os.path.isdir(full) else "FILE"
        try:
            size = os.path.getsize(full)
        except OSError:
            size = -1
        entries.append("{} {:>12}  {}".format(kind, size, name))
    return "\n".join(entries) if entries else "(empty directory)"


# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",
                           listing=None, listing_error=False,
                           script_output=None, script_error=False)


@app.route("/yarn-log", methods=["POST"])
def yarn_log():
    """Feature 1: Fetch yarn log and return as file download."""
    app_id   = request.form.get("app_id", "").strip()
    log_type = request.form.get("log_type", "full")

    if not app_id:
        return "Error: Application ID is required.", 400

    cmd = ["yarn", "logs", "-applicationId", app_id]
    stdout, stderr, rc = run_command(cmd)

    if rc != 0 and not stdout:
        return "Yarn error:\n" + stderr, 500

    # Filter for error lines only if requested
    if log_type == "error":
        lines = [l for l in stdout.splitlines() if "error" in l.lower()]
        content = "\n".join(lines) or "(no error lines found)"
    else:
        content = stdout or stderr

    # Save to temp file and stream back as download
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".log",
        prefix="{}_".format(app_id), mode="w"
    )
    tmp.write(content)
    tmp.close()

    filename = "{}_{}.log".format(app_id, log_type)
    return send_file(tmp.name, as_attachment=True, attachment_filename=filename)


@app.route("/list-dir", methods=["POST"])
def list_dir():
    """Feature 2: List directory contents and show on UI."""
    dir_path = request.form.get("dir_path", "").strip()

    if not dir_path:
        return render_template("index.html",
                               listing="Error: Directory path is required.",
                               listing_error=True,
                               script_output=None, script_error=False)
    try:
        listing = list_directory(dir_path)
        err = False
    except (ValueError, PermissionError) as e:
        listing = "Error: {}".format(e)
        err = True

    return render_template("index.html",
                           listing=listing, listing_error=err,
                           script_output=None, script_error=False)


@app.route("/run-script", methods=["POST"])
def run_script():
    """Feature 3: Execute a shell script and show stdout/stderr on UI."""
    script_path = request.form.get("script_path", "").strip()
    params_raw  = request.form.get("params", "").strip()

    if not script_path:
        return render_template("index.html",
                               script_output="Error: Script path is required.",
                               script_error=True,
                               listing=None, listing_error=False)

    if not os.path.exists(script_path):
        return render_template("index.html",
                               script_output="Error: Script not found: {}".format(script_path),
                               script_error=True,
                               listing=None, listing_error=False)

    # Split params safely — no shell expansion since shell=False
    params = params_raw.split() if params_raw else []
    cmd    = [script_path] + params

    stdout, stderr, rc = run_command(cmd)
    output = ""
    if stdout:
        output += "=== STDOUT ===\n" + stdout
    if stderr:
        output += "\n=== STDERR ===\n" + stderr
    if not output:
        output = "(no output)"

    err = (rc != 0)
    if err:
        output = "Exit code: {}\n\n".format(rc) + output

    return render_template("index.html",
                           script_output=output, script_error=err,
                           listing=None, listing_error=False)


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
