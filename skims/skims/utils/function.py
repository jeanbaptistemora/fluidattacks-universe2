# Standard library
from asyncio import (
    sleep,
)
import functools
import inspect
import traceback
from typing import (
    Any,
    Callable,
    cast,
    Tuple,
    Type,
    TypeVar,
)

# Third party libraries
import aioextensions
from more_itertools import (
    mark_ends,
)

# Local libraries
from utils.env import (
    guess_environment,
)
from utils.logs import (
    log,
    log_to_remote,
)

# Constants
RAISE = object()
RATE_LIMIT_ENABLED: bool = guess_environment() == 'production'
TFun = TypeVar('TFun', bound=Callable[..., Any])


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying.
    """


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
                    msg: str = 'Function: %s, %s: %s\n%s'
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    await log(
                        'warning',
                        msg,
                        function_id,
                        exc_type,
                        exc_msg,
                        traceback.format_exc(),
                    )
                    await log_to_remote(
                        exception=exc,
                        function_id=function_id,
                        exception_message=exc_msg,
                        exception_type=exc_type,
                    )

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


def rate_limited(*, rpm: float) -> Callable[[TFun], TFun]:
    if RATE_LIMIT_ENABLED:
        return aioextensions.rate_limited(
            max_calls=1,
            max_calls_period=60.0 / rpm,
            min_seconds_between_calls=60.0 / rpm,
        )

    return lambda x: x
