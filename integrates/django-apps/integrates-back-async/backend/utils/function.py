# Standard library
from typing import (
    Any,
    Callable,
)


def get_id(function: Callable[..., Any]) -> str:
    """Return a string identifying the provided function."""
    return f'{function.__module__} -> {function.__name__}'
