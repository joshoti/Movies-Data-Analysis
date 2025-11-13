import pytest
from fastapi.testclient import TestClient

from api.v2.app import create_app
from api.v2.services.db_client import get_db


@pytest.fixture(autouse=True, scope="session")
def db_ready():
    # Ensure CSV dataframe is loaded once per test session
    get_db().reload()
    yield


@pytest.fixture(scope="session")
def client():
    app = create_app()
    return TestClient(app)
