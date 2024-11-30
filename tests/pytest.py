from unittest.mock import patch
from fastapi.testclient import TestClient
from app.auth import create_access_token
from app.main import app

client = TestClient(app)
token = create_access_token(data={"sub": "test"})


def test_images_breed_success():
    breed_name = "bulldog"
    response = client.get(
        f"/dog/breed/{breed_name}", headers={"Authorization": f"Bearer {token}"})
    # Verifica que la respuesta sea exitosa
    assert response.status_code == 200
    assert "image" in response.json()
    assert "message" in response.json()


def test_images_breed_not_found():
    breed_name = "nonexistent_breed"
    response = client.get(
        f"/dog/breed/{breed_name}", headers={"Authorization": f"Bearer {token}"})
    # Verifica que la raza no exista
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid breed"}


def test_stats():
    # stats are available
    response = client.get(
        "/dog/stats", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "stats" in response.json()
    assert isinstance(response.json()["stats"], list)
    assert len(response.json()["stats"]) <= 10


def test_stats_no_data():
    # stats are not available
    with patch("app.database.MongoDB.get_top_breeds") as mock_get_top_breeds:
        mock_get_top_breeds.return_value = []
        response = client.get(
            "/dog/stats", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json() == {"stats": []}
