from pytest_bdd import given, when, then, scenarios
from uidom.front import Application, Window, Button
from uidom.front.drivers import gtk
from typing import Callable

scenarios("features/button_realization.feature")

@given("a UI DOM structure with a Window and a Button")
def given_a_ui_dom_structure_with_a_window_and_a_button(dom_application: Application) -> None:
    dom_application.windows.add(Window(title="Window", children=[Button(label="Button")]))

@when("the structure is realized")
def when_the_structure_is_realized(dom_application: Application, run_gtk_loop: Callable[[], None]) -> None:
    gtk.realize(dom_application)
    run_gtk_loop()

@then("the Button should be visible in the Window")
def then_the_button_should_be_visible_in_the_window(dom_application: Application) -> None:
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    gtk_button = gtk_window.get_child()
    assert gtk_button is not None
    assert gtk_button.get_visible()
    assert gtk_button.get_mapped()
    assert gtk_button.get_realized()
