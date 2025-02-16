import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_example():
    response = client.post(
        "/examples/",
        json={"name": "test example"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test example"

def test_read_examples():
    response = client.get("/examples/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_example():
    # First create an example
    create_response = client.post(
        "/examples/",
        json={"name": "test example"}
    )
    example_id = create_response.json()["id"]
    
    # Then read it
    response = client.get(f"/examples/{example_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "test example" 