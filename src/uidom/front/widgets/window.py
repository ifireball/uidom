from psygnal import Signal
from collections.abc import Iterable
from psygnal.containers import EventedSet
from .widget import Widget

class Window:
    """
    Represents a window on the screen.
    """
    closed = Signal()
    
    def __init__(self, title: str, children: Iterable[Widget] = []):
        self.title = title
        self.children = EventedSet(children)
        self.children.union(children)

    def close(self) -> None:
        self.closed.emit()
