import os

from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.environ.get(
    "MOVIES_DATASET_CSV", os.path.join("./data/external/MoviesDataset.csv")
)
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama2")
