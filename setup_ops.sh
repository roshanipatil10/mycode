#!/bin/bash
# setup_ops.sh — One-time setup: create venv and install Flask 2.0.3
# Usage: bash setup_ops.sh
# Run this ONCE before starting the app for the first time.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "[setup] Checking Python 3 availability..."
python3 --version || { echo "ERROR: python3 not found."; exit 1; }

echo "[setup] Creating virtual environment at $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

echo "[setup] Activating virtualenv..."
source "$VENV_DIR/bin/activate"

echo "[setup] Installing Flask 2.0.3..."
pip install --upgrade pip
pip install flask==2.0.3

echo ""
echo "[setup] Done! To start the app run:"
echo "        bash start_ops.sh"
