from dataclasses import dataclass
from typing import FrozenSet, TypeVar
from .widgets import Widget
from .utils import Visitor
from .style import Style

T = TypeVar("T")

@dataclass(frozen=True)
class Window:
    """
    Represents a window.
    """
    title: str = ""
    widgets: tuple[Widget, ...] = ()
    style: Style = Style()

    def visit(self, visitor: Visitor[T]) -> T:
        return visitor(self, *(widget.visit(visitor) for widget in self.widgets))
