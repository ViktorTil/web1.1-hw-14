from unittest.mock import MagicMock
from conftest import session

from src.database.models import User
from src.conf import messages


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    responce = client.post("/api/auth/signup", json=user)
    assert responce.status_code == 201, responce.text
    payload = responce.json()
    assert payload["user"]["email"] == user.get('email')
    
    
def test_repeat_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    responce = client.post("/api/auth/signup", json=user)
    assert responce.status_code == 409, responce.text
    payload = responce.json()
    assert payload["detail"] == messages.ACCOUNT_ALREADY_EXISTS
    
def test_login_user_not_confirmed_email(client, user):
    responce = client.post(
        "/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert responce.status_code == 401, responce.text
    payload = responce.json()
    assert payload["detail"] == messages.EMAIL_NOT_CONFIRMED
    
def test_login_user(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    responce = client.post(
        "/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert responce.status_code == 200, responce.text
    payload = responce.json()
    assert payload["token_type"] == "bearer"


def test_login_user_with_wrong_password(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    responce = client.post(
        "/api/auth/login", data={"username": user.get("email"), "password": "password"})
    assert responce.status_code == 401, responce.text
    payload = responce.json()
    assert payload["detail"] == messages.INVALID_PASSWORD


def test_login_user_with_wrong_email(client, user, session):
    current_user: User = session.query(User).filter(
        User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    responce = client.post(
        "/api/auth/login", data={"username": "example@test.com", "password": user.get("password")})
    assert responce.status_code == 401, responce.text
    payload = responce.json()
    assert payload["detail"] == messages.INVALID_EMAIL
