from __future__ import annotations

from typing import Protocol, Callable, TypeVar, TypeAlias

T = TypeVar("T")

class Visitable(Protocol):
    def visit(self, visitor: Visitor[T]) -> T:
        ...

class Visitor(Protocol[T]):
    def __call__(self, visitable: Visitable, /, *args: T) -> T:
        ...
