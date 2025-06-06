#!/bin/bash
# Simple environment setup script for AutoBaseDoc
# Creates a virtual environment and installs dependencies

set -e

ENV_DIR=".venv"
PYTHON=${PYTHON:-python3}

if [ ! -x "$(command -v $PYTHON)" ]; then
  echo "Python interpreter '$PYTHON' not found." >&2
  exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$ENV_DIR" ]; then
  $PYTHON -m venv "$ENV_DIR"
fi

# Activate the environment
source "$ENV_DIR/bin/activate"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Show some environment info
python info.py

echo "Virtual environment setup complete."
