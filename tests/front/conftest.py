import pytest
from uidom.front import Application

@pytest.fixture
def dom_application() -> Application:
    return Application()
