from fastapi.testclient import TestClient
from src.main import app
import src.tests.utils


setup_db = src.tests.utils.setup_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the PolygonFinder API"}


# Test creating a provider
def test_create_provider(setup_db):
    provider_data = {
        "name": "Test Provider",
        "email": "test@gmail.com",
        "phone_number": "+212634567890",
        "language": "en",
        "currency": "USD",
    }

    response = client.post("/api/v1/providers/", json=provider_data)

    assert response.status_code == 200
    assert response.json()["name"] == provider_data["name"]
    assert response.json()["email"] == provider_data["email"]
