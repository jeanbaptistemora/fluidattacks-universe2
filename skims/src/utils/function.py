# Standard library
import contextlib
import functools
from typing import (
    Any,
    Callable,
    cast,
    Tuple,
    Type,
    TypeVar,
)

# Constants
TVar = TypeVar('TVar')


def retry(
    *,
    attempts: int = 5,
    on_exceptions: Tuple[Type[Exception], ...] = (
        IndexError,
    ),
    on_error_return: Any = None,
) -> Callable[[TVar], TVar]:

    def decorator(function: TVar) -> TVar:

        _function = cast(Callable[..., Any], function)

        @functools.wraps(_function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(attempts):
                with contextlib.suppress(*on_exceptions):
                    return await _function(*args, **kwargs)

            return on_error_return

        return cast(TVar, wrapper)

    return decorator
