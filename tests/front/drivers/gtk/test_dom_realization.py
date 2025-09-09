from pytest_bdd import given, when, then, scenario
from uidom.front import Application, Window
import random
import pytest
from typing import Callable
from uidom.front.drivers import gtk

@scenario("features/dom_realization.feature", "Realize a Window")
def test_realize_a_window():
    pass

@pytest.fixture
def random_title() -> str:
    return f"Window {random.randint(1, 1000000)}"

@pytest.fixture
def dom_window(random_title: str) -> Window:
    """A UI DOM window with a random title."""
    return Window(title=random_title)

@given("a UI DOM structure with a Window")
def given_a_ui_dom_structure_with_a_window(dom_application: Application, dom_window: Window) -> None:
    dom_application.windows.add(dom_window)

@when("the structure is realized")
def when_the_structure_is_realized(dom_application: Application, run_gtk_loop: Callable[[], None]) -> None:
    gtk.realize(dom_application)
    run_gtk_loop()

@then("the Window should be visible on screen")
def then_the_window_should_be_visible_on_screen(dom_application: Application, dom_window: Window) -> None:
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    assert gtk_window.get_title() == dom_window.title
    assert gtk_window.get_visible()
    assert gtk_window.get_mapped()
    assert gtk_window.get_realized()

@when("the Window is closed")
def when_the_window_is_closed(dom_application: Application, dom_window: Window, run_gtk_loop: Callable[[], None]) -> None:
    dom_window.close()
    run_gtk_loop()

@then("the Window should be removed from the structure")
def then_the_window_should_be_removed_from_the_structure(dom_application: Application, dom_window: Window) -> None:
    assert dom_window not in dom_application.windows
    assert len(dom_application.windows) == 0

@then("the Window should be removed from the screen")
def then_the_window_should_be_removed_from_the_screen(dom_application: Application, dom_window: Window) -> None:
    assert len(gtk.gtk_windows) == 0
