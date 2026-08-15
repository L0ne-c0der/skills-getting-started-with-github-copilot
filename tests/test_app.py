from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_for_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]
    activities[activity_name]["participants"] = [
        participant for participant in original_participants if participant != email
    ]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activities[activity_name]["participants"] = [
        participant for participant in activities[activity_name]["participants"] if participant != email
    ]
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_invalid_activity_returns_404():
    # Arrange
    activity_name = "Missing Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
