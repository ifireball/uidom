from dataclasses import dataclass
from typing import FrozenSet
from .widgets import Widget
from .layouts import Layout, ColumnLayout

@dataclass(frozen=True)
class Window:
    """
    Represents a window.
    """
    title: str = ""
    widgets: FrozenSet[Widget] = frozenset()
    layout: Layout = ColumnLayout()
