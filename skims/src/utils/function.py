# Standard library
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
TVar = TypeVar('TVar')


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


def retry(
    *,
    attempts: int = 5,
    on_exceptions: Tuple[Type[Exception], ...],
    on_error_return: Any = None,
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

            if on_error_return:
                return on_error_return

            return await _function(*args, **kwargs)

        return cast(TVar, wrapper)

    return decorator
