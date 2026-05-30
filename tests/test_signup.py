def test_signup_adds_participant_and_returns_message(client):
    email = "newstudent@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant(client):
    duplicate_email = "michael@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": duplicate_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_requires_email_query_param(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
