from pytest_bdd import given, when, then, scenarios, parsers
from uidom.front import Application, Window, Button
from uidom.front.drivers import gtk
from typing import Callable, Hashable, Iterable
from uidom.front.drivers.gtk import Gtk

scenarios("features/layout_realization.feature")

@given(parsers.cfparse("a UI DOM structure with a Window and {n:int} Buttons", extra_types={"int": int}))
def given_a_ui_dom_structure_with_a_window_and_n_buttons(dom_application: Application, random_title: Callable[[Hashable], str], n: int) -> None:
    dom_application.windows.add(
        Window(title=random_title("Window"), children=[
            Button(text=random_title(f"Button {i}")) for i in range(n)
        ])
    )

@when("the structure is realized")
def when_the_structure_is_realized(dom_application: Application, run_gtk_loop: Callable[[], None]) -> None:
    gtk.realize(dom_application)
    run_gtk_loop()

@then("the buttons should be laid out vertically")
def then_the_buttons_should_be_laid_out_vertically(dom_application: Application, random_title: Callable[[Hashable], str], iterate_gtk_children: Callable[[Gtk.Widget], Iterable[Gtk.Widget]]) -> None:
    assert len(gtk.gtk_windows) == 1
    gtk_window = next(iter(gtk.gtk_windows))
    dom_window = next(iter(dom_application.windows))
    gtk_box = gtk_window.get_child()
    assert gtk_box is not None
    assert gtk_box.get_orientation() == Gtk.Orientation.VERTICAL
    gtk_box_children = list(iterate_gtk_children(gtk_box))
    assert len(gtk_box_children) == len(dom_window.children)
    for i, child in enumerate(gtk_box_children):
        assert child is not None
        assert isinstance(child, Gtk.Button)
        assert child.get_visible()
        assert child.get_mapped()
        assert child.get_realized()
        assert child.get_label() == random_title(f"Button {i}")
