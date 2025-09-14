import pytest
import time
from typing import Callable, Iterable
from uidom.front.drivers.gtk import GLib
from uidom.front import Application
from uidom.front.drivers import gtk
from uidom.front.drivers.gtk import Gtk


@pytest.fixture
def run_gtk_loop() -> Callable[[], None]:
    def run_loop():
        for _ in range(2):
            while GLib.MainContext.default().iteration(False):
                pass
            time.sleep(0.01)
    return run_loop


@pytest.fixture
def dom_application(run_gtk_loop: Callable[[], None]) -> Application:
    try:
        yield Application()
    finally:
        gtk.realize(Application())
        run_gtk_loop()

@pytest.fixture
def iterate_gtk_children() -> Callable[[Gtk.Widget], Iterable[Gtk.Widget]]:
    def iterate_children(widget: Gtk.Widget) -> Iterable[Gtk.Widget]:
        child = widget.get_first_child()
        while child is not None:
            yield child
            child = child.get_next_sibling()
    return iterate_children
