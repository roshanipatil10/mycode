# Daily Ops Runner

A minimal Flask web app for day-to-day DevOps operations on RHEL 7.9.
**Python 3.6 | Flask 2.0.3**

---

## Project Structure

```
ops_daily/
│
├── ops_runner.py          ← Main Flask application (routes + logic)
│
├── templates/
│   └── index.html         ← HTML UI (Jinja2 template)
│
├── setup_ops.sh           ← One-time setup: creates venv, installs Flask
├── start_ops.sh           ← Daily start script: activates venv, runs app
│
└── README.md              ← This file
```

### Why this structure?
| File | Purpose |
|---|---|
| `ops_runner.py` | All Python: Flask routes, subprocess calls, directory listing logic |
| `templates/index.html` | All HTML/CSS: the UI, completely separate from Python code |
| `setup_ops.sh` | Run **once** to create virtualenv and install Flask |
| `start_ops.sh` | Run **daily** to start the app — activates venv automatically |

---

## First-time Setup

```bash
cd ops_daily/
bash setup_ops.sh
```

## Start the App (daily)

```bash
bash start_ops.sh
```

Open in browser: `http://<server-ip>:5000`

## Stop the App

Press `Ctrl+C` in the terminal.

---

## Features

1. **Yarn Log Downloader** — fetches YARN app logs and downloads as `.log` file (full or error-filtered)
2. **File & Directory Listing** — lists any path on the server, shown inline in the browser
3. **Script Trigger** — runs any shell script with parameters; shows stdout/stderr in browser
