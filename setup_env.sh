#!/bin/bash

echo "========================================"
echo "ElderWise Environment Setup"
echo "========================================"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda first:"
    echo "https://www.anaconda.com/products/distribution"
    exit 1
fi

echo "Creating conda environment 'elderwise'..."
conda create -n elderwise python=3.11 -y

if [ $? -ne 0 ]; then
    echo "Error creating environment"
    exit 1
fi

echo ""
echo "Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate elderwise

echo ""
echo "Installing Python packages..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing packages"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your ElderWise environment is ready!"
echo ""
echo "To start the application:"
echo "1. Run: conda activate elderwise"
echo "2. Run: streamlit run app.py"
echo ""
echo "Or run: ./run.sh"
echo ""
