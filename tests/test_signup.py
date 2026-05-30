def test_signup_adds_participant_and_returns_message(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_requires_email_query_param(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
