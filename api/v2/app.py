from fastapi import FastAPI

from api.v2.routers import analysis, chat, query, rag


def create_app():
    app = FastAPI()

    app.include_router(analysis.router)
    app.include_router(query.router)
    app.include_router(chat.router)
    app.include_router(rag.router)

    return app
