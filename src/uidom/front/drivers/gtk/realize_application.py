from .driver import Gtk
from functools import partial
from uidom.front import Application
from .realize_children import realize_children


class GtkWindowSet:
    def __init__(self):
        self.windows = set()
    
    def add(self, window: Gtk.Window) -> None:
        self.windows.add(window)

    def remove(self, window: Gtk.Window) -> None:
        self.windows.remove(window)
        window.destroy()

    def __contains__(self, window: Gtk.Window) -> bool:
        return window in self.windows

    def __iter__(self):
        return iter(self.windows)
    
    def __len__(self) -> int:
        return len(self.windows)
    

gtk_windows = GtkWindowSet()


current_application = None


def realize(application: Application) -> None:
    global current_application
    if current_application is not None:
        current_application.close()
    current_application = application

    for gtk_window in list(gtk_windows):
        gtk_window.destroy()
        gtk_windows.remove(gtk_window)

    for window in application.windows:
        gtk_window = Gtk.Window(title=window.title)
        gtk_window.present()
        gtk_windows.add(gtk_window)
        window.closed.connect(partial(gtk_windows.remove, gtk_window))
        realize_children(window, gtk_window)
