from dataclasses import dataclass
from typing import FrozenSet, TypeVar
from .widgets import Widget
from .layouts import Layout, ColumnLayout
from .utils import Visitor

T = TypeVar("T")

@dataclass(frozen=True)
class Window:
    """
    Represents a window.
    """
    title: str = ""
    widgets: tuple[Widget, ...] = ()
    layout: Layout = ColumnLayout()

    def visit(self, visitor: Visitor[T]) -> T:
        return visitor(self, *(widget.visit(visitor) for widget in self.widgets))
