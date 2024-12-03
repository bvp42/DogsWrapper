from datetime import timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.auth import create_access_token
from app.main import app

client = TestClient(app)
token = create_access_token(data={"sub": "test"})


def create_expired_token():
    return create_access_token(data={"sub": "test"}, expires_delta=timedelta(days=-1))


def test_images_breed_success():
    with patch("app.database.MongoDB.insert_one") as mock_insert_one:
        # Simulate successful insertion (nothing returned)
        mock_insert_one.return_value = None

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
    with patch("app.database.MongoDB.get_top_breeds") as mock_get_top_breeds:
        mock_get_top_breeds.return_value = [
            {"_id": "labrador", "count": 10},
            {"_id": "bulldog", "count": 5},
            {"_id": "retriever", "count": 8}
        ]
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


def test_images_breed_invalid_auth():
    breed_name = "bulldog"
    response = client.get(f"/dog/breed/{breed_name}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_stats_invalid_auth():
    response = client.get("/dog/stats")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_user():
    with patch("app.database.MongoDBUsers.get_user") as mock_get_user:
        mock_get_user.return_value = None  # User does not exist
        with patch("app.database.MongoDBUsers.insert_one") as mock_insert_one:
            # Simulate successful insertion (nothing returned)
            mock_insert_one.return_value = None
            response = client.post(
                "/users", json={"username": "testuser", "password": "testpassword"})
            assert response.status_code == 200
            assert response.json() == {"message": "User created successfully"}


def test_create_user_existing_user():
    # Assuming the user already exists
    with patch("app.database.MongoDBUsers.get_user") as mock_get_user:
        mock_get_user.return_value = {
            "username": "testuser", "password": "testpassword"}
        response = client.post(
            "/users", json={"username": "testuser", "password": "testpassword"})
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exists"}


def test_login_for_access_token_success():
    with patch("app.auth.authenticate_user") as mock_authenticate_user:
        mock_authenticate_user.return_value = {
            "username": "testuser", "password": "testpassword"}
        response = client.post(
            "/token", data={"username": "testuser", "password": "testpassword"})
        assert response.status_code == 200


def test_login_for_access_token_invalid_user():
    with patch("app.auth.authenticate_user") as mock_authenticate_user:
        mock_authenticate_user.return_value = None
        response = client.post(
            "/token", data={"username": "testuser", "password": "testpassword"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}
