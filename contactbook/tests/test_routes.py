import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

client = TestClient(app)

@pytest.fixture
def user_data():
    return {"email": "testuser@example.com", "password": "password123"}

def test_register_user(user_data):
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_login_user(user_data):
    client.post("/users/register", json=user_data)
    response = client.post("/users/token", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route_without_token():
    response = client.get("/contacts/")
    assert response.status_code == 401
