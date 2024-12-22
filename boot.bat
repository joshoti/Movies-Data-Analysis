git clone https://github.com/joshoti/Movies-Data-Analysis.git
rm boot.bat
cd Movies-Data-Analysis

python -m venv venv

./venv/Scripts/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "\nSetup complete. Running app"

python app.py
