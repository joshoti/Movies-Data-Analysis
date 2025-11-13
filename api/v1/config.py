import os

from api.v1.extensions.swagger import swagger_config


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///movies.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    SWAGGER = swagger_config

    # Fallback to CPU to avoid NotImplementedError
    # for the 'aten::scatter_reduce.two_out' operator
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
