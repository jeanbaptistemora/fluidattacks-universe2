# Standard library
from typing import (
    Iterator,
)

# Third party libraries
import pytest


@pytest.fixture(scope='session')  # type: ignore
def test_group() -> Iterator[str]:
    yield 'worcester'
