# Standard libraries
import functools
from asyncio import sleep
from typing import (
    Any,
    Callable,
    cast,
    Tuple,
    Type,
    TypeVar,
)

# Third-party libraries
from more_itertools import mark_ends

# Local libraries
from utils.logs import log


# Constants
RAISE = object()
TFun = TypeVar('TFun', bound=Callable[..., Any])


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying.
    """


def shield(
    *,
    on_error_return: Any = RAISE,
    on_exceptions: Tuple[Type[BaseException], ...] = (
        BaseException,
        RetryAndFinallyReturn,
    ),
    retries: int = 1,
    sleep_between_retries: int = 0
) -> Callable[[TFun], TFun]:
    if retries < 1:
        raise ValueError('retries must be >= 1')

    def decorator(function: TFun) -> TFun:

        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = f'{function.__module__}.{function.__name__}'

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return await function(*args, **kwargs)
                except on_exceptions as exc:
                    msg: str = 'Function: %s, %s: %s'
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    await log('warning', msg, function_id, exc_type, exc_msg)

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    await log('info', 'retry #%s: %s', number, function_id)
                    await sleep(sleep_between_retries)

        return cast(TFun, wrapper)

    return decorator
