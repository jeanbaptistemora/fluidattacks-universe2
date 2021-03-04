# Standard library
from typing import (
    Any,
    Callable,
)


def get_id(function: Callable[..., Any], *extra: Any) -> str:
    """Return a string identifying the provided function.

    The parameter `*extra` will be used as part of the identifier.
    """
    return f'{function.__module__} -> {function.__name__}{extra}'
