from uidom.front import Application
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GioUnix', '2.0')
from gi.repository import Gtk
from gi.repository import GLib


class GtkWindowSet:
    def __init__(self):
        self.windows = set()
    
    def add(self, window: Gtk.Window) -> None:
        self.windows.add(window)

    def remove(self, window: Gtk.Window) -> None:
        window.destroy()
        self.windows.remove(window)

    def __contains__(self, window: Gtk.Window) -> bool:
        return window in self.windows

    def __iter__(self):
        return iter(self.windows)
    
    def __len__(self) -> int:
        return len(self.windows)
    

gtk_windows = GtkWindowSet()


def realize(application: Application) -> None:
    for window in application.windows:
        gtk_window = Gtk.Window(title=window.title)
        gtk_window.present()
        gtk_windows.add(gtk_window)
