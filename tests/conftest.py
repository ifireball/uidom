from collections.abc import Hashable
from functools import cache
from typing import Callable
import random
import pytest

@pytest.fixture
def random_title() -> Callable[[Hashable], str]:
    """A fixture that returns a function to generate a random title.
    The function is cached to return the same random title for the same key.
    """
    @cache
    def _random_title(key: Hashable) -> str:
        return f"{key} [{random.randint(1, 1000000)}]"
    return _random_title
