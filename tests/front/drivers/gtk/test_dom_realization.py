from pytest_bdd import given, when, then, scenarios
from uidom.front import Application, Window
import random
import pytest
from typing import Callable
from uidom.front.drivers import gtk
from unittest.mock import MagicMock

scenarios("features/dom_realization.feature")

@pytest.fixture
def random_title() -> str:
    return f"Window {random.randint(1, 1000000)}"

@pytest.fixture
def dom_window(random_title: str, run_gtk_loop: Callable[[], None]) -> Window:
    """A UI DOM window with a random title."""
    try:
        yield Window(title=random_title)
    finally:
        gtk.realize(Application())
        run_gtk_loop()

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
def then_the_window_should_be_removed_from_the_screen(dom_application: Application) -> None:
    assert len(gtk.gtk_windows) == 0

@pytest.fixture
def close_hook(dom_application: Application) -> Callable[[], None]:
    hook = MagicMock()
    dom_application.closed.connect(hook)
    return hook

@pytest.fixture
def window_close_hook(dom_window: Window) -> Callable[[], None]:
    hook = MagicMock()
    dom_window.closed.connect(hook)
    return hook

@when("an empty application is realized")
def when_an_empty_application_is_realized(run_gtk_loop: Callable[[], None], close_hook: MagicMock, window_close_hook: MagicMock) -> None:
    # Passing the close hook and window close hook to ensure they are connected
    # before the call gtk.realize() otherwise the hooks will not be in place
    # when the application and window are closed
    gtk.realize(Application())
    run_gtk_loop()

@then("the previous application should be closed")
def then_the_previous_application_should_be_closed(dom_application: Application, close_hook: MagicMock) -> None:
    assert close_hook.call_count == 1

@then("the Window should be closed")
def then_the_window_should_be_closed(dom_window: Window, window_close_hook: MagicMock) -> None:
    assert window_close_hook.call_count == 1
