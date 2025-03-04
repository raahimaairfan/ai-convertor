#!/bin/bash

# Ensure Python 3.10 is installed
sudo apt-get update && sudo apt-get install -y python3.10 python3.10-venv python3.10-dev

# Create a virtual environment in /home/appuser/
python3.10 -m venv /home/appuser/venv
source /home/appuser/venv/bin/activate

# Upgrade pip to avoid installation issues
pip install --upgrade pip

# Install the required dependencies
pip install spacy==3.5.3 thinc==8.1.10 numpy==1.23.5 cython==0.29.36

# Download the spaCy model
python -m spacy download en_core_web_sm
