from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    activity_names = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for name in activity_names:
        assert name in data


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Soccer Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    activity_data = client.get("/activities").json()[activity_name]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activity_data["participants"]

    # Cleanup
    client.delete(f"/activities/{activity_name}/participants?email={email}")


def test_signup_for_activity_rejects_duplicate_registration():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Unknown Club"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_participant_removes_student_from_activity():
    # Arrange
    activity_name = "Track and Field"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    activity_data = client.get("/activities").json()[activity_name]

    # Assert
    assert response.status_code == 200
    assert email not in activity_data["participants"]


def test_delete_participant_for_missing_student_returns_404():
    # Arrange
    activity_name = "Art Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()
