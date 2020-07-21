# Standard library
import asyncio
import collections.abc
import functools
from typing import (
    Any,
    cast,
    Callable,
    Tuple,
    TypeVar,
)

# Third party libraries
from more_itertools import chunked

# Constants
TVar = TypeVar('TVar')


async def materialize(obj: Any, batch_size: int = 128) -> Any:
    materialized_obj: Any

    # Please use abstract base classes:
    #   https://docs.python.org/3/glossary.html#term-abstract-base-class
    #
    # Pick them up here according to the needed interface:
    #   https://docs.python.org/3/library/collections.abc.html
    #

    if isinstance(obj, collections.abc.Mapping):
        materialized_obj = dict(zip(
            obj,
            await materialize(obj.values()),
        ))
    elif isinstance(obj, collections.abc.Iterable):
        materialized_obj = [
            await awaitable
            for awaitables in chunked(obj, batch_size)
            for awaitable in [
                (
                    elem
                    if isinstance(elem, asyncio.Future)
                    else asyncio.create_task(elem)
                )
                for elem in awaitables
            ]
        ]
    else:
        raise ValueError(f'Not implemented for type: {type(obj)}')

    return materialized_obj


async def unblock(
    function: Callable[..., TVar],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    return await asyncio.get_running_loop().run_in_executor(
        None, functools.partial(function, *args, **kwargs),
    )


async def unblock_many(
    functions: Tuple[Callable[[], TVar], ...],
) -> Tuple[TVar, ...]:
    loop = asyncio.get_running_loop()

    results: Tuple[TVar, ...] = await materialize(
        loop.run_in_executor(None, function) for function in functions
    )

    return results


async def unblock_decorator(function: TVar) -> TVar:
    _function: Callable[..., TVar] = cast(Callable[..., TVar], function)

    @functools.wraps(_function)
    async def _wrapper(*args: Any, **kwargs: Any) -> TVar:
        return await unblock(_function, *args, **kwargs)

    return cast(TVar, _wrapper)
