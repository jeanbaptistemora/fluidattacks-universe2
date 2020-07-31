# Standard library
import asyncio
import collections.abc
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
import functools
from os import (
    cpu_count,
)
from typing import (
    Any,
    Awaitable,
    cast,
    Callable,
    TypeVar,
)

# Third party libraries
from more_itertools import chunked
import uvloop

# Constants
CPU_COUNT: int = cpu_count() or 1
TVar = TypeVar('TVar')

# Executors
PROCESS_POOL = ProcessPoolExecutor(max_workers=CPU_COUNT)
THREAD_POOL = ThreadPoolExecutor(max_workers=10 * CPU_COUNT)


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
        THREAD_POOL, functools.partial(function, *args, **kwargs),
    )


async def unblock_cpu(
    function: Callable[..., TVar],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    return await asyncio.get_running_loop().run_in_executor(
        PROCESS_POOL, functools.partial(function, *args, **kwargs),
    )


def block(
    function: Callable[..., Awaitable[TVar]],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    uvloop.install()
    return asyncio.run(function(*args, **kwargs))


def block_decorator(function: TVar) -> TVar:
    _function = cast(Callable[..., Any], function)

    @functools.wraps(_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return block(_function, *args, **kwargs)

    return cast(TVar, wrapper)
