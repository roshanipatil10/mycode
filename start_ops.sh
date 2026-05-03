#!/bin/bash
# start_ops.sh — Start the Daily Ops Runner Flask app
# Usage: bash start_ops.sh
# Place this file in the same directory as ops_runner.py

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
APP="$SCRIPT_DIR/ops_runner.py"

# ── Activate virtualenv if present ─────────────────────────────────────────
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "[ops] Activating virtualenv..."
    source "$VENV_DIR/bin/activate"
else
    echo "[ops] WARNING: No venv found at $VENV_DIR — using system Python 3"
fi

# ── Verify Flask is installed ───────────────────────────────────────────────
python3 -c "import flask" 2>/dev/null || {
    echo "[ops] ERROR: Flask not found. Run: pip install flask==2.0.3"
    exit 1
}

# ── Launch app ──────────────────────────────────────────────────────────────
echo "[ops] Starting Daily Ops Runner on http://0.0.0.0:5000 ..."
python3 "$APP"
