import aioextensions
from asyncio import (
    sleep,
)
from asyncio.tasks import (
    wait_for,
)
import functools
import inspect
from metaloaders.model import (
    Node,
)
from more_itertools import (
    mark_ends,
)
import traceback
from typing import (
    Any,
    Callable,
    cast,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)
from utils.env import (
    guess_environment,
)
from utils.logs import (
    log,
)

# Constants
RAISE = object()
RATE_LIMIT_ENABLED: bool = guess_environment() == "production"
TFun = TypeVar("TFun", bound=Callable[..., Any])


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying."""


class SkimsCanNotOperate(Exception):
    """Skims cannot operate at this time."""


def get_bound_arguments(
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> inspect.BoundArguments:
    signature: inspect.Signature = get_signature(function)
    arguments: inspect.BoundArguments = signature.bind(*args, **kwargs)
    arguments.apply_defaults()

    return arguments


def get_id(function: Callable[..., Any]) -> str:
    if isinstance(function, functools.partial):
        function = function.func

    return f"{function.__module__}.{function.__name__}"


def get_signature(function: Callable[..., Any]) -> inspect.Signature:
    signature: inspect.Signature = inspect.signature(
        function,
        follow_wrapped=True,
    )

    return signature


def get_node_by_keys(node: Node, keys: List[str]) -> Optional[Node]:
    cur_node = node
    for key in keys:
        if key in cur_node.inner:
            cur_node = cur_node.inner[key]
        else:
            return None
    return cur_node


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
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = get_id(function)

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return await function(*args, **kwargs)
                except on_exceptions as exc:
                    msg: str = "Function: %s, %s: %s\n%s"
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    await log(
                        "warning",
                        msg,
                        function_id,
                        exc_type,
                        exc_msg,
                        traceback.format_exc(),
                    )

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    await log("info", "retry #%s: %s", number, function_id)
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


def pipe(value: Any, *functions: Callable[..., Any]) -> Any:
    for function in functions:
        value = function(value)

    return value


def time_limited(
    *,
    seconds: Optional[int] = None,
) -> Callable[[TFun], TFun]:
    def decorator(function: TFun) -> TFun:
        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await wait_for(
                function(*args, **kwargs),
                timeout=seconds,
            )

        return cast(TFun, wrapper)

    return decorator


# Constants
TIMEOUT_1MIN: Callable[[TFun], TFun] = time_limited(seconds=60)
