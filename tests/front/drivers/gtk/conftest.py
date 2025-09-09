import pytest
import time
from typing import Callable
from uidom.front.drivers.gtk import GLib


@pytest.fixture
def run_gtk_loop() -> Callable[[], None]:
    def run_loop():
        for _ in range(2):
            while GLib.MainContext.default().iteration(False):
                pass
            time.sleep(0.01)
    return run_loop
