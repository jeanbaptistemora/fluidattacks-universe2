# Standard library
from asyncio import (
    sleep,
    Lock,
)
import functools
import inspect
from typing import (
    Any,
    Callable,
    cast,
    Tuple,
    Type,
    TypeVar,
)

# Local libraries
from utils.logs import (
    log,
)

# Constants
RAISE = object()
TVar = TypeVar('TVar')
TFun = TypeVar('TFun', bound=Callable[..., Any])


def get_bound_arguments(
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> inspect.BoundArguments:
    signature: inspect.Signature = get_signature(function)
    arguments: inspect.BoundArguments = signature.bind(*args, **kwargs)
    arguments.apply_defaults()

    return arguments


def get_signature(function: Callable[..., Any]) -> inspect.Signature:
    signature: inspect.Signature = inspect.signature(
        function, follow_wrapped=True,
    )

    return signature


def locked(function: TFun) -> TFun:
    lock = Lock()

    @functools.wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with lock:
            return await function(*args, **kwargs)

    return cast(TFun, wrapper)


def retry(
    *,
    attempts: int = 5,
    on_error: Any = RAISE,
    on_exceptions: Tuple[Type[Exception], ...],
    sleep_between_retries: int = 0
) -> Callable[[TVar], TVar]:

    def decorator(function: TVar) -> TVar:

        _function = cast(Callable[..., Any], function)

        @functools.wraps(_function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(attempts):
                try:
                    return await _function(*args, **kwargs)
                except on_exceptions:
                    await log('debug', 'retrying: %s', _function.__name__)
                    await sleep(sleep_between_retries)

            if on_error is RAISE:
                return await _function(*args, **kwargs)

            return on_error

        return cast(TVar, wrapper)

    return decorator
