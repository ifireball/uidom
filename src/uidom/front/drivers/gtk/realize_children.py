from .driver import Gtk
from uidom.front import Window, Button, Widget, StringDisplay


def realize_children(parent: Window, gtk_parent: Gtk.Window) -> None:
    if len(parent.children) == 0:
        return
    if len(parent.children) == 1:
        child = next(iter(parent.children))
        gtk_parent.set_child(realize_widget(child))
        return
    gtk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    gtk_parent.set_child(gtk_box)
    for child in parent.children:
        gtk_box.append(realize_widget(child))

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
    
