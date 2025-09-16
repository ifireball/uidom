from psygnal import Signal
from collections.abc import Iterable
from psygnal.containers import EventedList
from .widget import Widget
from ..layouts.layout import Layout
from ..layouts.column import ColumnLayout

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
