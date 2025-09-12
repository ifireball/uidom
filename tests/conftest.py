from collections.abc import Hashable
from functools import cache
from typing import Callable
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
def random_callback() -> Callable[[Hashable], Callable[[], None]]:
    """A fixture that returns a function to generate a random callback.
    The function is cached to return the same random callback for the same key.
    """
    @cache
    def _random_callback(key: Hashable) -> Callable[[], None]:
        return MagicMock()
    return _random_callback 
