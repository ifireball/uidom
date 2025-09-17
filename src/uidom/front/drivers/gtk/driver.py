import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GioUnix', '2.0')
from gi.repository import Gtk  # type: ignore
from gi.repository import GLib  # type: ignore
_ = Gtk, GLib
