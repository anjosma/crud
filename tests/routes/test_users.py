import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.user import User

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["is_active"] is True

def test_create_user_duplicate_email(client: TestClient, test_user: User):
    response = client.post(
        "/users/",
        json={"name": "Another User", "email": test_user.email}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_users(client: TestClient, test_user: User):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == test_user.id
    assert data["items"][0]["name"] == test_user.name
    assert data["items"][0]["email"] == test_user.email

def test_read_user(client: TestClient, test_user: User):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == test_user.name
    assert data["email"] == test_user.email

def test_read_user_not_found(client: TestClient):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_user(client: TestClient, test_user: User):
    response = client.put(
        f"/users/{test_user.id}",
        json={"name": "Updated Name", "email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == "Updated Name"
    assert data["email"] == "updated@example.com"

def test_update_user_not_found(client: TestClient):
    response = client.put(
        "/users/999",
        json={"name": "Updated Name", "email": "updated@example.com"}
    )
    assert response.status_code == 404

def test_delete_user(client: TestClient, test_user: User):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 404

def test_delete_user_not_found(client: TestClient):
    response = client.delete("/users/999")
    assert response.status_code == 404