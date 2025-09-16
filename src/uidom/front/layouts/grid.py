from .layout import Layout
from dataclasses import dataclass

@dataclass(frozen=True)
class GridLayout(Layout):
    """
    Layout for a grid of widgets.
    """
    size: int = 2
