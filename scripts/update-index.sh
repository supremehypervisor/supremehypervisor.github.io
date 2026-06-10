#!/usr/bin/env bash
# update-index.sh — Orbital Index auto-updater (bash wrapper)
# Delegates to the Python script. Run from repo root:
#   bash scripts/update-index.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/update-index.py" --root "$ROOT" "$@"
else
    echo "[orbital] Error: python3 not found. Install Python 3.6+ and retry."
    exit 1
fi
