def test_unregister_removes_participant_and_returns_message(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"
    email = "not-in-club@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in activity"}


def test_unregister_requires_email_query_param(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422
