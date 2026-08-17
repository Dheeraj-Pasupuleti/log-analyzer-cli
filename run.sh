#!/bin/bash

set -e

echo "======================================"
echo "       Log Analyzer Setup"
echo "======================================"

if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "Python: $(python3 --version)"

# Create virtual environment and install dependencies
# only on the first run
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv

    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        .venv/bin/python -m pip install -r requirements.txt
    fi

    echo "Setup completed."
fi

echo "======================================"
echo "       Running Log Analyzer"
echo "======================================"

.venv/bin/python main.py "$@"