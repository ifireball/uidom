from .driver import Gtk
from uidom.front import Window, Button, Widget, StringDisplay
from uidom.model.layouts import ColumnLayout, GridLayout
from typing import Iterable


def realize_children(parent: Window, gtk_parent: Gtk.Window) -> None:
    if len(parent.children) == 0:
        return
    if len(parent.children) == 1:
        child = next(iter(parent.children))
        gtk_parent.set_child(realize_widget(child))
        return
    match parent.layout:
        case ColumnLayout():
            child = realize_column_layout(parent.children)
        case GridLayout(size=size):
            child = realize_grid_layout(parent.children, size)
        case _:
            raise ValueError(f"Unknown layout: {parent.layout}")
    gtk_parent.set_child(child)

def realize_column_layout(children: Iterable[Widget]) -> Gtk.Widget:
    gtk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    for child in children:
        gtk_box.append(realize_widget(child))
    return gtk_box

def realize_grid_layout(children: Iterable[Widget], size: int) -> Gtk.Widget:
    gtk_grid = Gtk.Grid()
    for index, child in enumerate(children):
        row = index // size
        column = index % size
        gtk_grid.attach(realize_widget(child), column, row, 1, 1)
    return gtk_grid



def realize_widget(widget: Widget) -> Gtk.Widget:
    match widget:
        case Button():
            button = Gtk.Button(label=widget.text)
            button.connect("clicked", widget.clicked.emit)
            return button
        case StringDisplay():
            label = Gtk.Label(label=widget.text)
            return label
        case _:
            raise ValueError(f"Unknown widget: {widget}")
    
