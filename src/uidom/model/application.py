from dataclasses import dataclass
from typing import FrozenSet, TypeVar
from .window import Window
from .utils import Visitor

T = TypeVar("T")

@dataclass(frozen=True)
class Application:
    """
    Represents an application.
    """
    windows: FrozenSet[Window] = frozenset()

    def visit(self, visitor: Visitor[T]) -> T:
        return visitor(self, *(window.visit(visitor) for window in self.windows))   
