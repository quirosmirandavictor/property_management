from fastapi.testclient import TestClient

from rentmanager.main import app


def test_login_and_me() -> None:
    client = TestClient(app)

    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json() == {"username": "admin"}
