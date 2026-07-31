import uuid


# ==========================
# User Endpoints
# ==========================

def test_get_user_me(client, test_user):
    client.post(
        "/auth/register",
        json=test_user
    )

    login_response = client.post(
        "/auth/login",
        json=test_user
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_user["name"]


def test_users(client, admin_user):
    login_response = client.post(
        "/auth/login",
        json=admin_user
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200


def test_get_user(client, admin_user, test_user):
    register_response = client.post(
        "/auth/register",
        json=test_user
    )

    user_id = register_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json=admin_user
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id


def test_delete_user(client, admin_user, test_user):
    register_response = client.post(
        "/auth/register",
        json=test_user
    )

    user_id = register_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json=admin_user
    )

    access_token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id

    check_response = client.get(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert check_response.status_code == 404


def test_update_user_name(client, admin_user, test_user):
    register_response = client.post(
        "/auth/register",
        json=test_user
    )

    user_id = register_response.json()["id"]

    new_name = f"arthas_{uuid.uuid4()}"

    login_response = client.post(
        "/auth/login",
        json=admin_user
    )

    access_token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{user_id}/name",
        json={
            "name": new_name
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == new_name


def test_update_user_password(client, admin_user, test_user):
    register_response = client.post(
        "/auth/register",
        json=test_user
    )

    user_id = register_response.json()["id"]

    old_password = test_user["password"]
    new_password = "1488"

    login_response = client.post(
        "/auth/login",
        json=admin_user
    )

    access_token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{user_id}/password",
        json={
            "old_password": old_password,
            "new_password": new_password
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user_id

    old_login = client.post(
        "/auth/login",
        json={
            "name": test_user["name"],
            "password": old_password
        }
    )

    assert old_login.status_code == 401

    new_login = client.post(
        "/auth/login",
        json={
            "name": test_user["name"],
            "password": new_password
        }
    )

    assert new_login.status_code == 200