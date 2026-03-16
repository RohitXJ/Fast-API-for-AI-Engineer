import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from app.main import app, get_session

# Use an IN-MEMORY SQLite database for tests (No files, no lock errors!)
# StaticPool is required for in-memory DBs to keep the connection open across the test
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

def override_get_session():
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    # Create the tables in the memory DB
    SQLModel.metadata.create_all(engine)
    app.dependency_overrides[get_session] = override_get_session
    
    with TestClient(app) as c:
        yield c
    
    # Just clear the data, no files to remove
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()

def test_signup(client):
    response = client.post("/signup", params={"username": "newuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["msg"] == "User created successfully"

def test_login_and_predict(client):
    client.post("/signup", params={"username": "predictuser", "password": "password123"})
    
    login_response = client.post("/login", data={"username": "predictuser", "password": "password123"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    prediction_response = client.post("/predict", json={"feature_vector": [1.0, 2.0, 3.0]}, headers=headers)
    assert prediction_response.status_code == 200
    assert "prediction" in prediction_response.json()

def test_unauthorized_predict(client):
    response = client.post("/predict", json={"feature_vector": [1.0]})
    assert response.status_code == 401
