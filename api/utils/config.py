import os


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
