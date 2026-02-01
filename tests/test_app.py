import os
import sys
import pytest

# Ensure `src` is importable
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

from fastapi.testclient import TestClient

from app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity
    assert "Basketball Team" in data


def test_signup_and_unregister_flow(client):
    activity_name = "Chess Club"
    test_email = "test_student@example.com"

    # Ensure clean state for this test
    orig_participants = list(activities[activity_name]["participants"])
    if test_email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(test_email)

    # Signup
    signup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert signup_resp.status_code == 200
    assert test_email in activities[activity_name]["participants"]

    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister", params={"email": test_email})
    assert unregister_resp.status_code == 200
    assert test_email not in activities[activity_name]["participants"]

    # Restore original state
    activities[activity_name]["participants"] = orig_participants
