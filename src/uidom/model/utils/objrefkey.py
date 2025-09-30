from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any, Callable, Generic, TypeAlias, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, eq=False, slots=True)
class ObjRefKey(Generic[T]):
    """
    A simple, immutable wrapper to an object, meant to be used as a dictionary
    key referring to that object.

    >>> obj = object()
    >>> key = ObjRefKey(obj)
    >>> key.obj is obj
    True
    >>> key is obj
    False
    >>> key == ObjRefKey(obj)
    False
    >>> key is ObjRefKey(obj)
    False
    >>> from typing import Hashable
    >>> isinstance(key, Hashable)
    True
    >>> key.obj = object()
    Traceback (most recent call last):
    ...
    dataclasses.FrozenInstanceError: cannot assign to field 'obj'
    """
    obj: T

    def unwrap(self) -> T:
        """Convenience method to get the object back from the key.

        >>> obj = object()
        >>> key = ObjRefKey(obj)
        >>> key.unwrap() is obj
        True
        """
        return self.obj

    def __lt__(self, other: ObjRefKey[T]) -> bool:
        return id(self) < id(other)
    
    def __le__(self, other: ObjRefKey[T]) -> bool:
        return id(self) <= id(other)
    
    def __gt__(self, other: ObjRefKey[T]) -> bool:
        return id(self) > id(other)
    
    def __ge__(self, other: ObjRefKey[T]) -> bool:
        return id(self) >= id(other)


ObjRefKeyMaker: TypeAlias = Callable[[T], ObjRefKey[T]]


def objRefKeySet() -> ObjRefKeyMaker[T]:
    """
    Returns a function that creates and manages a set of object reference keys.

    >>> A = objRefKeySet()
    >>> B = objRefKeySet()

    Given the following objects:

    >>> obj1 = object()
    >>> obj2 = object()
    >>> a1 = A(obj1)
    >>> a2 = A(obj2)
    >>> b1 = B(obj1)

    We can expect the following:

    >>> isinstance(a1, ObjRefKey)
    True
    >>> isinstance(a2, ObjRefKey)
    True
    >>> isinstance(b1, ObjRefKey)
    True
    >>> a1 is A(obj1)
    True
    >>> a1 is a2
    False
    >>> a1 is obj1
    False
    >>> a1 is b1
    False
    >>> a1 == b1
    False
    
    We can get the object back from the key with unwrap():

    >>> a1.unwrap() == obj1
    True
    """
    return cache(ObjRefKey[T])
