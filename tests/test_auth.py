from fastapi.testclient import TestClient


def test_register_user(client: TestClient, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201


def test_login_user(client: TestClient, test_user):
    client.post("/auth/register", json=test_user)
    response = client.post("/auth/login", json=test_user)
    data = response.json()

    assert response.status_code == 200
    assert "refresh_token" in data


def test_refresh_token(client: TestClient, test_user):
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", json=test_user)
    data = login_response.json()
    refresh_token = data["refresh_token"]

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    refresh_data = response.json()

    assert response.status_code == 200
    assert "access_token" in refresh_data


def test_logout_user(client: TestClient, test_user):
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", json=test_user)
    data = login_response.json()
    refresh_token = data["refresh_token"]

    response = client.post("/auth/logout", json={"refresh_token": refresh_token})

    assert response.status_code == 204


def test_refresh_after_logout_fails(client: TestClient, test_user):
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", json=test_user)
    data = login_response.json()
    refresh_token = data["refresh_token"]

    logout_response = client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert logout_response.status_code == 204

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 401