import aioextensions
from asyncio import (
    sleep,
)
import functools
from more_itertools import (
    mark_ends,
)
from toolbox.utils.env import (
    guess_environment,
)
from toolbox.utils.logs import (
    log,
    log_to_remote,
)
from typing import (
    Any,
    Callable,
    cast,
    Tuple,
    Type,
    TypeVar,
)

# Constants
RAISE = object()
TFun = TypeVar("TFun", bound=Callable[..., Any])
RATE_LIMIT_ENABLED: bool = guess_environment() == "production"


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying."""


def shield(
    *,
    on_error_return: Any = RAISE,
    on_exceptions: Tuple[Type[BaseException], ...] = (
        BaseException,
        RetryAndFinallyReturn,
    ),
    retries: int = 1,
    sleep_between_retries: int = 0,
) -> Callable[[TFun], TFun]:
    if retries < 1:
        raise ValueError("retries must be >= 1")

    def decorator(function: TFun) -> TFun:
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = f"{function.__module__}.{function.__name__}"

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return function(*args, **kwargs)
                except on_exceptions as exc:
                    msg: str = "Function: %s, %s: %s"
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    log("warning", msg, function_id, exc_type, exc_msg)
                    log_to_remote(exc)

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    log("info", "retry #%s: %s", number, function_id)
                    sleep(sleep_between_retries)
                    return None

        return cast(TFun, wrapper)

    return decorator


def rate_limited(*, rpm: float) -> Callable[[TFun], TFun]:
    if RATE_LIMIT_ENABLED:
        return aioextensions.rate_limited(
            max_calls=1,
            max_calls_period=60.0 / rpm,
            min_seconds_between_calls=60.0 / rpm,
        )
    return lambda x: x
