from abc import ABC
from dataclasses import dataclass
from typing import Callable

class Widget(ABC):
    """
    Base class for all widgets.
    """

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
