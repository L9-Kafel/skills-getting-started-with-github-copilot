import copy
import warnings

import pytest

# Suppress Starlette deprecation warning caused by TestClient/httpx bridge
try:
    from starlette.exceptions import StarletteDeprecationWarning

    warnings.filterwarnings("ignore", category=StarletteDeprecationWarning)
except Exception:
    # If Starlette isn't available for some reason, skip the filter
    pass

from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def isolate_activities():
    """Ensure `activities` in `src.app` is reset between tests.

    We deepcopy the original data and restore it after each test so tests
    don't leak state via the in-memory store.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture()
def client():
    original_activities = deepcopy(activities)

    with TestClient(app) as test_client:
        yield test_client

    activities.clear()
    activities.update(deepcopy(original_activities))