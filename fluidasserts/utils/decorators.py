# -*- coding: utf-8 -*-

"""This module enables decorators for registry and usage tracking purposes."""

# standard imports
import sys
import functools
from timeit import default_timer as timer
from typing import Callable, Any
from .tracking import mp_track

# 3rd party imports
import oyaml as yaml

# local imports
from fluidasserts import Result

OUTFILE = sys.stderr


def _get_func_id(func: Callable) -> str:
    """Return a function identifier."""
    return f"{func.__module__} -> {func.__name__}"


def api(risk: str, kind: str) -> Callable:
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


def track(func: Callable) -> Callable:
    """Log and register function usage."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Any:  # noqa
        """Log and registers function usage."""
        mp_track(_get_func_id(func))
        return func(*args, **kwargs)
    return decorated


def level(risk_level: str) -> Callable:
    """Create decorator factory."""
    def wrapper(func: Callable) -> Callable:
        """Give a risk level to each check."""
        @functools.wraps(func)
        def decorated(*args, **kwargs) -> Any:  # noqa
            """Give a risk level to each check."""
            ret_val = func(*args, **kwargs)
            risk = {'risk': risk_level}
            message = yaml.safe_dump(risk,
                                     default_flow_style=False,
                                     explicit_start=False,
                                     allow_unicode=True)
            print(message, flush=True)
            return ret_val
        return decorated
    return wrapper


def notify(func: Callable) -> Callable:
    """Notify the user that the function is running."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Any:  # noqa
        """Notify the user that the function is running."""
        print(f'  check: {_get_func_id(func)}', file=sys.stderr, flush=True)
        ret_val = func(*args, **kwargs)
        return ret_val
    return decorated
