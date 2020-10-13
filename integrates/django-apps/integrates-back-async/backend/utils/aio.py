# Standard library
from asyncio import (
    Future,
    get_running_loop,
)
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
import functools
from typing import (
    Any,
    Awaitable,
    cast,
    Coroutine,
    Callable,
    NamedTuple,
    TypeVar,
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
class PyCallable(NamedTuple):  # pylint:disable=too-few-public-methods
    instance: Callable
    args: tuple = tuple()
    kwargs: frozendict = frozendict()


# Typing
TypeT = TypeVar('TypeT')


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


def to_async(
    function: Callable[..., TypeT],
) -> Callable[..., Awaitable[TypeT]]:

    @functools.wraps(function)
    async def wrapper(*args: str, **kwargs: Any) -> Any:
        return await ensure_io_bound(function, *args, **kwargs)

    return cast(Callable[..., Awaitable[TypeT]], wrapper)
