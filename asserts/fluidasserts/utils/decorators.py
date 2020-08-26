# -*- coding: utf-8 -*-

"""This module enables decorators for registry and usage tracking purposes."""

# standard imports
import sys
import functools
from typing import Any, Callable
from timeit import default_timer as timer

# local imports
from fluidasserts import Result, UNKNOWN
from fluidasserts.utils.tracking import mp_track


def _get_func_id(func: Callable) -> str:
    """Return a function identifier."""
    return f"{func.__module__} -> {func.__name__}"


# pylint: disable=unused-argument
def api(risk: str, kind: str, **kwargs: Any) -> Callable:
    """Pre-processing and post-processing of the function results."""
    def wrapper(func: Callable) -> Callable:
        """Return a wrapper to the decorated function."""
        @functools.wraps(func)
        def decorated(*args, **kwargs) -> Any:  # noqa
            """Pre-process and post-process the function results."""
            # Instantiate the result object
            result = Result(risk=risk, kind=kind,
                            func=func, func_args=args, func_kwargs=kwargs)

            # Notify that the check is running
            print(f'  check: {result.func_id}', file=sys.stderr, flush=True)

            # Track the function
            mp_track(result.func_id)

            # Run the function
            start_time = timer()
            status, message, *extra = func(*args, **kwargs)
            end_time = timer()
            duration = round(end_time - start_time, 2)

            # Append the results to the Result object
            result.set_status(status)
            result.set_message(message)
            result.set_duration(duration)
            result.set_vulns(extra.pop(0) if extra else [])
            result.set_safes(extra.pop(0) if extra else [])

            # Register it to the stats
            result.register_stats()

            # Print
            result.print()

            # Return a Result object with rich information
            return result
        return decorated
    return wrapper


def unknown_if(*errors) -> Callable:
    """Return UNKNOWN if a function raise one of the provided errors."""
    def wrapper(func: Callable) -> Callable:
        """Return a wrapper to the decorated function."""
        @functools.wraps(func)
        def decorated(*args, **kwargs) -> Any:
            """Wrap the function in a try except block."""
            try:
                result = func(*args, **kwargs)
            except errors as exc:
                return UNKNOWN, f'An error occurred: {exc}'
            return result
        return decorated
    return wrapper


def track(func: Callable) -> Callable:
    """Log and register function usage."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Any:  # noqa
        """Log and registers function usage."""
        mp_track(_get_func_id(func))
        return func(*args, **kwargs)
    return decorated
