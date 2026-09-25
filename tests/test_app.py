from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "tester@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
