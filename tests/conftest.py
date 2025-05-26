import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def authenticated_client():
    class MockUser:
        def __init__(self):
            self.id = 1
            self.email = "test@example.com"
            self.is_active = True
            self.password = "mocked_hashed_password"
            self.is_admin = True

    def override_get_current_user():
        return MockUser()

    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
