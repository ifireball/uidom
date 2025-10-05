from __future__ import annotations

from .utils.sparse_attribute import Sparse
from .layouts import Layout, ColumnLayout
from dataclasses import dataclass

@dataclass(frozen=True)
class Style:
    """
    Represents a style for a window or a widget.
    """
    layout: Sparse[Layout] = Sparse[Layout](default=ColumnLayout())
