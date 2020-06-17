# Standard library
from asyncio import (
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
async def ensure_many_cpu_bound(py_callables: List[PyCallable]) -> Future:
    return await _ensure_many(ProcessPoolExecutor, py_callables)


@apm.trace()
async def ensure_many_io_bound(py_callables: List[PyCallable]) -> Future:
    return await _ensure_many(ThreadPoolExecutor, py_callables)


@apm.trace()
async def ensure_cpu_bound(py_callable: PyCallable) -> Future:
    return (await _ensure_many(ProcessPoolExecutor, [py_callable]))[0]


@apm.trace()
async def ensure_io_bound(py_callable: PyCallable) -> Future:
    return (await _ensure_many(ThreadPoolExecutor, [py_callable]))[0]


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
