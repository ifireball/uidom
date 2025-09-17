from dataclasses import dataclass
from typing import FrozenSet
from .window import Window

@dataclass(frozen=True)
class Application:
    """
    Represents an application.
    """
    windows: FrozenSet[Window] = frozenset()

