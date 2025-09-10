from collections.abc import Iterable
from typing import Tuple

from psygnal import Signal
from .window import Window
from psygnal.containers import EventedSet
from functools import partial

class Application:
    """
    A top-level application container.
    """

    closed = Signal()

    def __init__(self, windows: Iterable[Window] = []):
        self.windows = EventedSet(windows)
        self.windows.events.items_changed.connect(self.on_windows_changed)
        self.windows.union(windows)
    
    def on_windows_changed(self, added: Tuple[Window, ...], removed: Tuple[Window, ...]) -> None:
        for window in added:
            window.closed.connect(partial(self.windows.remove, window))

    def close(self) -> None:
        for window in list(self.windows):
            window.close()
        self.closed.emit()
