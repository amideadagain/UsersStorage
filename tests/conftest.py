import pytest_asyncio
from starlette.testclient import TestClient

from src.main import app


@pytest_asyncio.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
