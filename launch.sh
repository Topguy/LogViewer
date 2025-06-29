#!/bin/bash
# This script is used to launch the LogViewer application.

# It is recommended to create and activate a virtual environment before running.
# For example:
# python -m venv .venv
# source .venv/bin/activate

# Get the directory where this script is located.
SCRIPT_DIR=$(dirname -- "$0")

# Run the main application file.
python "$SCRIPT_DIR/logviewer/app.py"