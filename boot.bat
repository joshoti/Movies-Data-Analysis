git clone https://github.com/joshoti/Movies-Data-Analysis.git
rm boot.bat
cd Movies-Data-Analysis

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv venv --python 3.12

./.venv/Scripts/activate

uv pip install --upgrade pip
uv sync --no-dev --group api-v2-deps

echo -e "\nSetup complete. Running app"

uvicorn main_v2:app --host 0.0.0.0 --port 8000