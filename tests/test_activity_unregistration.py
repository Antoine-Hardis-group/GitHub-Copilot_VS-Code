from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def setup_function():
    activities["Soccer Team"]["participants"] = []


def test_unregister_participant_removes_email_from_activity():
    email = "student@mergington.edu"

    signup_response = client.post("/activities/Soccer Team/signup?email=student@mergington.edu")
    assert signup_response.status_code == 200
    assert email in activities["Soccer Team"]["participants"]

    delete_response = client.delete("/activities/Soccer Team/unregister?email=student@mergington.edu")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from Soccer Team"
    assert email not in activities["Soccer Team"]["participants"]


def test_unregister_missing_participant_returns_error():
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/Soccer Team/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"{email} is not signed up for Soccer Team"
