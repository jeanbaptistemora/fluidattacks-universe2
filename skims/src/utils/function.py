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

# Third party libraries
from more_itertools import (
    mark_ends,
)

# Local libraries
from utils.logs import (
    log,
)

# Constants
RAISE = object()
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


def never_concurrent(function: TFun) -> TFun:
    """Ensure the decorated function runs at max once at any point in time.

    :param function: Function to decorate
    :type function: TFun
    :return: A function capped to be executed at most once at any point in time
    :rtype: TFun
    """
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
) -> Callable[[TFun], TFun]:
    if attempts < 1:
        raise ValueError('attempts must be >= 1')

    def decorator(function: TFun) -> TFun:

        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = f'{function.__module__}.{function.__name__}'

            for _, is_last, number in mark_ends(range(attempts)):
                try:
                    return await function(*args, **kwargs)
                except on_exceptions as exc:
                    msg: str = 'Function: %s, %s: %s'
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    await log('info', msg, function_id, exc_type, exc_msg)

                    if is_last:
                        if on_error is RAISE:
                            raise exc
                        return on_error

                    await log('info', 'retry #%s: %s', number, function_id)
                    await sleep(sleep_between_retries)

        return cast(TFun, wrapper)

    return decorator
