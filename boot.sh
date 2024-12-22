#!/bin/bash

git clone https://github.com/joshoti/Movies-Data-Analysis.git
rm boot.sh
cd Movies-Data-Analysis

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "\nSetup complete. Running app"

python app.py
