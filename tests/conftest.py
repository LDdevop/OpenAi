import pytest
from flask_api.app import app


@pytest.fixture()
def client():
    return app.test_client()
