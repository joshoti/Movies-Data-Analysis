#!/bin/bash

git clone https://github.com/joshoti/Movies-Data-Analysis.git
cd Movies-Data-Analysis

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To run app, run 1. 'source venv/bin/activate' 2. 'python app.py' in terminal"
