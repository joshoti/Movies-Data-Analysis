#!/bin/bash

git clone https://github.com/joshoti/Movies-Data-Analysis.git
rm boot.sh
cd Movies-Data-Analysis

curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.12

source .venv/bin/activate

uv pip install --upgrade pip
uv sync --no-dev --group api-v2-deps

echo -e "\nSetup complete. Running app"

python app.py
