from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def setup_function():
    activities["Soccer Team"]["participants"] = []


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Soccer Team"
    email = "student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert precondition
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Act
    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_error():
    # Arrange
    activity_name = "Soccer Team"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"{email} is not signed up for {activity_name}"
