from abc import ABC
from dataclasses import dataclass
from typing import TypeVar
from .utils import Visitor

T = TypeVar("T")

class Widget(ABC):
    """
    Base class for all widgets.
    """
    def visit(self, visitor: Visitor[T]) -> T:
        return visitor(self)

@dataclass(frozen=True)
class Button(Widget):
    """
    Represents a button on the screen.
    """
    text: str = ""


@dataclass(frozen=True)
class StringDisplay(Widget):
    """
    Represents a string display on the screen.
    """
    text: str = ""
