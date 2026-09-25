#!/bin/bash

# Circle City Model - Run Script
# ================================

echo "=========================================="
echo "Circle City Model - Web Application"
echo "=========================================="
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python is not installed."
    exit 1
fi

echo "Using Python: $PYTHON"
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed."
    exit 1
fi

echo "Checking dependencies..."

# Check and install numpy
if $PYTHON -c "import numpy" 2>/dev/null; then
    echo "✓ numpy is installed"
else
    echo "Installing numpy..."
    pip install numpy
fi

# Check and install flask
if $PYTHON -c "import flask" 2>/dev/null; then
    echo "✓ flask is installed"
else
    echo "Installing flask..."
    pip install flask
fi

echo ""
echo "All dependencies are ready!"
echo ""
echo "Starting the application..."
echo ""

# Run the application
$PYTHON app.py
