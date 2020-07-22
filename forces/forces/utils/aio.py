"""Fluid Forces AIO helper."""
# Standard library
import asyncio
import functools
from typing import (
    Any,
    Callable,
    TypeVar,
)

# Constants
TVar = TypeVar('TVar')


async def unblock(
        function: Callable[..., TVar],
        *args: Any,
        **kwargs: Any,
) -> TVar:
    """Run a funcion in asyncio eventloop executor."""
    return await asyncio.get_running_loop().run_in_executor(
        None,
        functools.partial(function, *args, **kwargs),
    )
