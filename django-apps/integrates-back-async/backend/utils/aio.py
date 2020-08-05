# Standard library
from asyncio import (
    create_task,
    Future,
    gather,
    get_running_loop,
)
import collections.abc
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
import functools
from multiprocessing import cpu_count
from typing import (
    Any,
    Awaitable,
    cast,
    Coroutine,
    Callable,
    List,
    NamedTuple,
    TypeVar,
    Union,
)

# Third party libraries
from frozendict import frozendict
from more_itertools import chunked

# Local libraries
from backend.utils import (
    apm,
)


# Containers
# I'm using a class because this is the only way to pass default values
# It is still an immutable typed wonderfully awesome NamedTuple
class PyCallable(NamedTuple):  # pylint:disable=too-few-public-methods
    instance: Callable
    args: tuple = tuple()
    kwargs: frozendict = frozendict()


# Typing
TypeT = TypeVar('TypeT')


@apm.trace()
async def ensure_many_cpu_bound(py_callables: List[PyCallable]) -> Coroutine:
    return await _ensure_many(ProcessPoolExecutor, py_callables)


@apm.trace()
async def ensure_many_io_bound(py_callables: List[PyCallable]) -> Coroutine:
    return await _ensure_many(ThreadPoolExecutor, py_callables)


@apm.trace()
async def ensure_cpu_bound(function: Callable, *args, **kwargs) -> Coroutine:
    return await _ensure_one(ProcessPoolExecutor, PyCallable(
        instance=function,
        args=tuple(args),
        kwargs=frozendict(kwargs),
    ))


@apm.trace()
async def ensure_io_bound(function: Callable, *args, **kwargs) -> Coroutine:
    return await _ensure_one(ThreadPoolExecutor, PyCallable(
        instance=function,
        args=tuple(args),
        kwargs=frozendict(kwargs),
    ))


@apm.trace()
async def _ensure_one(
    executor_class: Union[ProcessPoolExecutor, ThreadPoolExecutor],
    py_callable: PyCallable,
) -> Future:
    with executor_class(max_workers=1) as pool:  # type: ignore
        loop = get_running_loop()

        return await loop.run_in_executor(
            pool,
            functools.partial(
                py_callable.instance,
                *py_callable.args,
                **py_callable.kwargs,
            ),
        )


@apm.trace()
async def _ensure_many(
    executor_class: Union[ProcessPoolExecutor, ThreadPoolExecutor],
    py_callables: List[PyCallable],
) -> Future:
    # Leave one worker to the main event loop, be gently with it
    with executor_class(max_workers=cpu_count() - 1) as pool:  # type: ignore
        loop = get_running_loop()

        return await gather(*[
            loop.run_in_executor(
                pool,
                functools.partial(
                    py_callable.instance,
                    *py_callable.args,
                    **py_callable.kwargs,
                )
            )
            for py_callable in py_callables
        ])


@apm.trace()
async def materialize(obj: Any, batch_size: int = 128) -> Any:
    """
    Turn any awaitable and possibly nested-object into a real object.

    It takes care of doing so concurrently, event for nested objects.

    This function is particularly useful to cache values,
    because non-materialized futures, coroutines or tasks cannot be sent
    to redis.
    """
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
                    if isinstance(elem, Future)
                    else create_task(elem)
                )
                for elem in awaitables
            ]
        ]
    else:
        raise ValueError(f'Not implemented for type: {type(obj)}')

    return materialized_obj


def to_async(
    function: Callable[..., TypeT],
) -> Callable[..., Awaitable[TypeT]]:

    @functools.wraps(function)
    async def wrapper(*args: str, **kwargs: Any) -> Any:
        return await ensure_io_bound(function, *args, **kwargs)

    return cast(Callable[..., Awaitable[TypeT]], wrapper)
