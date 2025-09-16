from .layout import Layout
from dataclasses import dataclass

@dataclass(frozen=True)
class ColumnLayout(Layout):
    """
    Layout for a column of widgets.
    """
