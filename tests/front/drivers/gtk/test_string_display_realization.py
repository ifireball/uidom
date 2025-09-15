from pytest_bdd import given, when, then, scenarios
from uidom.front import Application, Window, StringDisplay
from uidom.front.drivers import gtk
from typing import Callable, Hashable
from uidom.front.drivers.gtk import Gtk

scenarios("features/string_display_realization.feature")

@given("a UI DOM structure with a Window and a String Display with some random text")
def given_a_ui_dom_structure_with_a_window_and_a_string_display_with_some_random_text(dom_application: Application, random_title: Callable[[Hashable], str]) -> None:
    dom_application.windows.add(Window(title=random_title("Window"), children=[StringDisplay(text=random_title("String Display"))]))

@when("the structure is realized")
def when_the_structure_is_realized(dom_application: Application, run_gtk_loop: Callable[[], None]) -> None:
    gtk.realize(dom_application)
    run_gtk_loop()

@then("the String Display should be visible in the Window as a Gtk.Label")
def then_the_string_display_should_be_visible_in_the_window_as_a_gtk_label(random_title: Callable[[Hashable], str]) -> None:
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    gtk_label = gtk_window.get_child()
    assert gtk_label is not None
    assert isinstance(gtk_label, Gtk.Label)

@then("the String Display should have the random text")
def then_the_string_display_should_have_the_random_text(random_title: Callable[[Hashable], str]) -> None:
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    gtk_label = gtk_window.get_child()
    assert gtk_label is not None
    assert gtk_label.get_label() == random_title("String Display")
