import json
from datetime import date

from src.models.user.crud import User as UserCrud
from src.utils.hashing import bcrypt


def test_create_user(test_app, monkeypatch):
    test_request_payload = {
        "username": "string",
        "email": "user@example.com",
        "password": "string"
    }
    test_response_payload = {"message": "user created successfully"}

    async def mock_post(user):
        return True

    monkeypatch.setattr(UserCrud, "post", mock_post)

    response = test_app.post("/user/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_user_invalid_json(test_app):
    response = test_app.post(
        "/user/",
        data=json.dumps({"username": "string"})
    )
    assert response.status_code == 422


def test_create_user_with_taken_email_or_username(test_app, monkeypatch):
    test_request_payload = {
        "username": "string",
        "email": "user@example.com",
        "password": "$2b$12$3Qz.gNkyHo1qZyGfgxWj0uv/SqqR6PUeFIWgr9JNKMgUFIuzgHJHu"
    }
    test_response_payload = {"message": "username or email already taken"}

    async def mock_post(user):
        return False

    monkeypatch.setattr(UserCrud, "post", mock_post)

    response = test_app.post("/user/", data=json.dumps(test_request_payload),)

    assert response.status_code == 409
    assert response.json() == test_response_payload


def test_get_user(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "username": "string",
        "email": "user@example.com",
        "password": bcrypt("string"),
        "register_date": str(date.today())
    }

    async def mock_get(user_id):
        return test_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    response = test_app.get("/user/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(user_id):
        return None

    monkeypatch.setattr(UserCrud, "get", mock_get)

    response = test_app.get("/user/10")
    assert response.status_code == 404
    assert response.json() == {"message": "user not found"}


def test_update_user(test_app, monkeypatch):
    test_update_data = {
        "username": "string",
        "email": "user@example.com",
        "password": "$2b$12$3Qz.gNkyHo1qZyGfgxWj0uv/SqqR6PUeFIWgr9JNKMgUFIuzgHJHu",
        "register_date": "2022-02-01"
    }

    async def mock_get(user_id):
        return test_update_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_put(user_id, user):
        return True

    monkeypatch.setattr(UserCrud, "put", mock_put)

    response = test_app.put("/user/1", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == {"message": "user data updated successfully"}


def test_update_user_username_or_email_taken(test_app, monkeypatch):
    test_update_data = {
        "username": "string",
        "email": "user@example.com",
        "password": "$2b$12$3Qz.gNkyHo1qZyGfgxWj0uv/SqqR6PUeFIWgr9JNKMgUFIuzgHJHu",
        "register_date": "2022-02-01"
    }

    async def mock_get(user_id):
        return test_update_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_put(user_id, user):
        return False

    monkeypatch.setattr(UserCrud, "put", mock_put)

    response = test_app.put("/user/1", data=json.dumps(test_update_data))
    assert response.status_code == 409
    assert response.json() == {"message": "username or email already taken"}


def test_patch_user(test_app, monkeypatch):
    test_update_data = {
        "password": "$2b$12$3Qz.gNkyHo1qZyGfgxWj0uv/SqqR6PUeFIWgr9JNKMgUFIuzgHJHu",
        "register_date": "2022-02-01"
    }

    async def mock_get(user_id):
        return test_update_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_patch(user_id, user):
        return True

    monkeypatch.setattr(UserCrud, "patch", mock_patch)

    response = test_app.patch("/user/1", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == {"message": "user data updated successfully"}


def test_patch_user_username_or_email_taken(test_app, monkeypatch):
    test_update_data = {
        "username": "string",
        "email": "user@example.com"
    }

    async def mock_get(user_id):
        return test_update_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_patch(user_id, user):
        return False

    monkeypatch.setattr(UserCrud, "patch", mock_patch)

    response = test_app.patch("/user/1", data=json.dumps(test_update_data))
    assert response.status_code == 409
    assert response.json() == {"message": "username or email already taken"}


def test_delete_user(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "username": "string",
        "email": "user@example.com",
        "password": bcrypt("string"),
        "register_date": str(date.today())
    }

    async def mock_get(user_id):
        return test_data

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_delete(user_id):
        return True

    monkeypatch.setattr(UserCrud, "delete", mock_delete)

    response = test_app.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == {"message": "user data deleted successfully"}


def test_delete_user_invalid_id(test_app, monkeypatch):
    async def mock_get(user_id):
        return None

    monkeypatch.setattr(UserCrud, "get", mock_get)

    async def mock_delete(user_id):
        return True

    monkeypatch.setattr(UserCrud, "delete", mock_delete)

    response = test_app.delete("/user/1")
    assert response.status_code == 404
    assert response.json() == {"message": "user not found"}


def test_get_user_list(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "username": "string",
            "email": "user@example.com",
            "password": "$2b$12$3pAF2Tu0Krv.g15QdLFNKuoxfo3CQxg1a0jDgYzoX.2JratFiedi6",
            "register_date": "2022-02-01"
        },
        {
            "id": 2,
            "username": "trv",
            "email": "svdfc@example.com",
            "password": "$2b$12$Q6jsQl2CDO2dzjMoWRzlAe/deF8wFA6nsqmOOFtVbvOS8HTLFjMXO",
            "register_date": "2022-02-01"
        }
    ]

    async def mock_get_list():
        return test_data

    monkeypatch.setattr(UserCrud, "get_list", mock_get_list)

    response = test_app.get("/user-list/")
    assert response.status_code == 200
    assert response.json() == test_data
