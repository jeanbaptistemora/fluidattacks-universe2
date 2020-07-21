# Standard library
import asyncio
import collections.abc
from typing import (
    Any,
    TypeVar,
)

# Constants
TVar = TypeVar('TVar')


async def materialize(obj: Any) -> Any:
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
            await awaitable for awaitable in [
                elem
                if isinstance(elem, asyncio.Future)
                else asyncio.create_task(elem)
                for elem in obj
            ]
        ]
    else:
        raise ValueError(f'Not implemented for type: {type(obj)}')

    return materialized_obj
