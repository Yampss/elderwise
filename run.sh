#!/bin/bash
echo "Starting ElderWise - Connecting Generations Through Stories"
echo ""
echo "Please make sure you have your Gemini API key ready!"
echo "You can get one free at: https://makersuite.google.com/app/apikey"
echo ""
echo "Activating conda environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda first"
    exit 1
fi

# Activate the environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate elderwise

if [ $? -ne 0 ]; then
    echo "Error: Could not activate elderwise environment. Creating it now..."
    conda create -n elderwise python=3.11 -y
    conda activate elderwise
    pip install -r requirements.txt
fi

echo ""
echo "Starting the application..."
streamlit run app.py --server.port 8501
