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

@given("a UI DOM structure with a Window")
def given_a_ui_dom_structure_with_a_window(dom_application: Application, random_title: str):
    dom_application.windows.append(Window(title=random_title))

@when("the structure is realized")
def when_the_structure_is_realized(dom_application: Application, run_gtk_loop: Callable[[], None]):
    gtk.realize(dom_application)
    run_gtk_loop()

@then("the Window should be visible on screen")
def then_the_window_should_be_visible_on_screen(dom_application: Application):
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    assert gtk_window.get_title() == dom_application.windows[0].title
    assert gtk_window.get_visible()
    assert gtk_window.get_mapped()
    assert gtk_window.get_realized()
