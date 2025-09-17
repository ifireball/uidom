from psygnal import Signal
from collections.abc import Iterable
from psygnal.containers import EventedList
from .widget import Widget
from uidom.model.layouts import Layout, ColumnLayout


class Window:
    """
    Represents a window on the screen.
    """
    closed = Signal()
    
    def __init__(self, title: str, children: Iterable[Widget] = [], layout: Layout = ColumnLayout()):
        self.title = title
        self.children = EventedList(children)
        self.layout = layout

    def close(self) -> None:
        self.closed.emit()
