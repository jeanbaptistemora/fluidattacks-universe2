# Standard library
from asyncio import (
    create_task,
    Future,
    gather,
    get_running_loop,
)
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
import functools
from multiprocessing import cpu_count
from typing import (
    Coroutine,
    Callable,
    List,
    NamedTuple,
    Union,
)

# Third party libraries
from frozendict import frozendict

# Local libraries
from backend.utils import (
    apm,
)


# Containers
# I'm using a class because this is the only way to pass default values
# It is still an immutable typed wonderfully awesome NamedTuple
class PyCallable(NamedTuple):
    instance: Callable
    args: tuple = tuple()
    kwargs: frozendict = frozendict()


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
async def materialize(obj: object) -> object:
    """Turn any awaitable and possibly nested-object into a real object.

    It takes care of doing so concurrently, event for nested objects.

    This function is particularly useful to cache values,
    because non-materialized futures, coroutines or tasks cannot be sent
    to redis.
    """
    materialized_obj: object

    if isinstance(obj, (dict, frozendict)):
        materialized_obj = \
            dict(zip(obj, await materialize(tuple(obj.values()))))
    elif isinstance(obj, (list, tuple)):
        materialized_obj = \
            await gather(*tuple(map(create_task, obj)))
    else:
        raise ValueError(f'Not implemented for type: {type(obj)}')

    return materialized_obj
