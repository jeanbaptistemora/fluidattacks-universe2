"""Fluid Forces AIO helper."""
# Standard library
import asyncio
from typing import (
    Any,
    Awaitable,
    Callable,
    TypeVar,
)

# Third party libraries
import uvloop

# Constants
TVar = TypeVar('TVar')


def block(
    function: Callable[..., Awaitable[TVar]],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    uvloop.install()
    return asyncio.run(function(*args, **kwargs))
