import pytest
from litestar.testing import TestClient

from backend.src.app import app


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app=app) as client:
        yield client
