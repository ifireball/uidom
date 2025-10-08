from dataclasses import dataclass
from typing import FrozenSet, TypeVar
from .widgets import Widget
from .utils import Visitor
from .style import Style, Styleable

T = TypeVar("T")

@dataclass(frozen=True, kw_only=True)
class Window(Styleable):
    """
    Represents a window.
    """
    title: str = ""
    widgets: tuple[Widget, ...] = ()

    def visit(self, visitor: Visitor[T]) -> T:
        return visitor(self, *(widget.visit(visitor) for widget in self.widgets))
