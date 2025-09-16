from dotenv import load_dotenv
from fastapi import FastAPI

from api.routers import analysis, inference, query, rag

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.include_router(analysis.router)
app.include_router(query.router)
app.include_router(inference.router)
app.include_router(rag.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
