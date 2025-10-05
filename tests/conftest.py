from collections.abc import Hashable
from functools import cache
from typing import Callable, Mapping
from collections import defaultdict
import random
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def random_title() -> Callable[[Hashable], str]:
    """A fixture that returns a function to generate a random title.
    The function is cached to return the same random title for the same key.
    """
    @cache
    def _random_title(key: Hashable) -> str:
        return f"{key} [{random.randint(1, 1000000)}]"
    return _random_title

@pytest.fixture
def enumerated_title() -> Callable[[str], str]:
    """A fixture that returns a function to generate an enumerated titles
    so that each time a key is passed we get a title with a higher number.
    """
    title_cache = defaultdict[str, int](int)

    def _enumerated_title(key: str) -> str:
        num = title_cache[key]
        title_cache[key] = num + 1
        return f"{key} {num}"
    return _enumerated_title

@pytest.fixture
def random_callback() -> Callable[[Hashable], Callable[[], None]]:
    """A fixture that returns a function to generate a random callback.
    The function is cached to return the same random callback for the same key.
    """
    @cache
    def _random_callback(key: Hashable) -> Callable[[], None]:
        return MagicMock()
    return _random_callback 
