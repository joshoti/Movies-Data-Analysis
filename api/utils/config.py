import os

from flask import Flask
from flask_cors import CORS

from api.extensions.db import db


class Config:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///movies.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    # Fallback to CPU to avoid NotImplementedError
    # for the 'aten::scatter_reduce.two_out' operator
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


def create_flask_app(name: str):
    app = Flask(name)

    # Configure app
    app.config.from_object(Config)

    # Register extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:3000"])

    return app
