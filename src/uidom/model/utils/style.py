from typing import Any
from uidom.model.positions import GridPosition
from uidom.model.style import Styleable

def colspan(widget: Any) -> int:
    """
    Return the horizontal span of a widget within a grid layout.

    >>> from uidom.model import Button
    >>> from uidom.model.style import Style
    >>> from uidom.model.positions import GridPosition
    >>> colspan(Button(style=Style(position=GridPosition(horizontal_span=2))))
    2

    >>> colspan(Button())
    1

    We use very lax typing here to make this helper useful in various places.

    >>> colspan(object())
    1
    """
    match widget:
        case Styleable():
            match widget.style.position:
                case GridPosition(horizontal_span=span):
                    return span
    return 1
