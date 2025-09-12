from psygnal import Signal
from .widget import Widget
from typing import Callable

class Button(Widget):
    """
    Represents a button on the screen.
    """
    #: The signal emitted when the button is clicked.
    clicked = Signal()

    def __init__(self, text: str, clicked: Callable[[], None] = None):
        self.text = text
        self.clicked.connect(clicked)
