from asyncio import (
    sleep,
)
from contextlib import (
    suppress,
)
from ctx import (
    TOOLS_SEMVER_MATCH,
)
from custom_exceptions import (
    InvalidVulnerableVersion,
)
import functools
import inspect
import json
from metaloaders.model import (
    Node,
)
from more_itertools import (
    mark_ends,
)
import sys
from time import (
    sleep as sleep_blocking,
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
    log_blocking,
    log_to_remote,
    log_to_remote_blocking,
)
from utils.system import (
    read_blocking,
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
        function_attributes = function.func
    else:
        function_attributes = function

    return f"{function_attributes.__module__}.{function_attributes.__name__}"


def get_signature(function: Callable[..., Any]) -> inspect.Signature:
    signature: inspect.Signature = inspect.signature(
        function,
        follow_wrapped=True,
    )

    return signature


def get_node_by_keys(node: Node, keys: List[str]) -> Optional[Node]:
    cur_node = node
    for key in keys:
        if hasattr(cur_node, "inner") and key in cur_node.inner:
            with suppress(TypeError):
                cur_node = cur_node.inner[key]
        else:
            return None
    return cur_node


def get_dict_values(dict_val: dict, *keys: str) -> Optional[Any]:
    cur_dict = dict_val
    for key in keys:
        if key in cur_dict:
            cur_dict = cur_dict[key]
        else:
            return None
    return cur_dict


def semver_match(left: str, right: str, exc: bool = False) -> bool:
    code, out, _ = read_blocking(TOOLS_SEMVER_MATCH, left, right)

    if code == 0:
        data = json.loads(out)
        if data["success"]:
            return data["match"]
        if exc:
            raise InvalidVulnerableVersion()
        log_blocking(
            "error",
            "Semver match %s to %s: %s",
            left,
            right,
            data["error"],
        )
    elif exc:
        raise InvalidVulnerableVersion()
    else:
        log_blocking("error", "Semver match %s to %s", left, right)

    return False


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
                    exc_type, exc_value, exc_taceback = sys.exc_info()
                    await log_to_remote(
                        msg=(exc_type, exc_value, exc_taceback),
                        severity="error",
                        function_id=function_id,
                        retry=number,  # type: ignore
                    )

                    msg: str = "Function: %s, %s: %s\n%s"
                    await log(
                        "warning",
                        msg,
                        function_id,
                        type(exc_type).__name__,
                        exc_value,
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


def shield_blocking(
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
        def wrapper(  # pylint: disable=inconsistent-return-statements
            *args: Any, **kwargs: Any
        ) -> Any:
            function_id = get_id(function)

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return function(*args, **kwargs)
                except on_exceptions as exc:
                    exc_type, exc_value, exc_taceback = sys.exc_info()
                    log_to_remote_blocking(
                        msg=(exc_type, exc_value, exc_taceback),
                        severity="error",
                        function_id=function_id,
                        retry=number,  # type: ignore
                    )

                    msg: str = "Function: %s, %s: %s\n%s"
                    log_blocking(
                        "warning",
                        msg,
                        function_id,
                        type(exc_type).__name__,
                        exc_value,
                        traceback.format_exc(),
                    )

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    log_blocking("info", "retry #%s: %s", number, function_id)
                    sleep_blocking(sleep_between_retries)

        return cast(TFun, wrapper)

    return decorator
