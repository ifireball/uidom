from __future__ import annotations

from .utils.sparse_attribute import Sparse
from .layouts import Layout, ColumnLayout
from dataclasses import dataclass
from .positions import Position, AutoPosition
import abc

@dataclass(frozen=True)
class Style:
    """
    Represents a style for a window or a widget.
    """
    layout: Sparse[Layout] = Sparse[Layout](default=ColumnLayout())
    position: Sparse[Position] = Sparse[Position](default=AutoPosition())

@dataclass(frozen=True, kw_only=True)
class Styleable:
    """
    Mixing class for objects that have a style.
    """
    style: Style = Style()
