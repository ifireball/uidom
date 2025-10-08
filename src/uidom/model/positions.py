import abc
from dataclasses import dataclass

class Position(abc.ABC):
    """
    Base class for all positions.
    Positions are style attributes that are used to determine the position of
    a widget within a parent.
    """

class AutoPosition(Position):
    """
    Represents a position that is automatically determined by the parent's layout.
    """

@dataclass(frozen=True)
class GridPosition(Position):
    """
    Influence positioning within a grid layout.
    """
    horizontal_span: int = 1
    
