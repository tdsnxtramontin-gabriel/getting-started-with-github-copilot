from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

_BASELINE_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Ensure each test gets a clean in-memory activities dataset."""
    activities.clear()
    activities.update(deepcopy(_BASELINE_ACTIVITIES))
    yield


@pytest.fixture
def client():
    return TestClient(app)
