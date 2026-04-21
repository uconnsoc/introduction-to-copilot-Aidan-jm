from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data  # Check if a known activity exists

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=dup@example.com")
    # Second signup (should fail)
    response = client.post("/activities/Chess%20Club/signup?email=dup@example.com")
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_delete_success():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=del@example.com")
    # Then delete
    response = client.delete("/activities/Programming%20Class/signup?email=del@example.com")
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

def test_delete_not_registered():
    response = client.delete("/activities/Programming%20Class/signup?email=notreg@example.com")
    assert response.status_code == 400
    result = response.json()
    assert "Student not registered" in result["detail"]

def test_delete_activity_not_found():
    response = client.delete("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]