import abc
from dataclasses import dataclass

class Layout(abc.ABC):
    """
    Base class for all layouts.
    """

@dataclass(frozen=True)
class ColumnLayout(Layout):
    """
    Layout for a column of widgets.
    """

@dataclass(frozen=True)
class GridLayout(Layout):
    """
    Layout for a grid of widgets.
    """
    size: int = 2
