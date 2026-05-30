def test_unregister_removes_participant_and_returns_message(client):
    email = "michael@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-in-club@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in activity"}


def test_unregister_requires_email_query_param(client):
    response = client.delete("/activities/Chess%20Club/participants")

    assert response.status_code == 422
