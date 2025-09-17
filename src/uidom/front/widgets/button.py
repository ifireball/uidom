from psygnal import Signal
from .widget import Widget
from typing import Callable, Optional

class Button(Widget):
    """
    Represents a button on the screen.
    """
    #: The signal emitted when the button is clicked.
    clicked = Signal()

    def __init__(self, text: str, clicked: Optional[Callable[[], None]] = None):
        self.text = text
        if clicked is not None:
            self.clicked.connect(clicked)
