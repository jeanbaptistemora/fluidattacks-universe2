# Local imports
from typing import Any
from toolbox import constants


def debug(*args: Any, **kwargs: Any) -> None:
    """Logger for debug category."""
    if constants.LOGGER_DEBUG:
        print('[DEBUG]', *args, **kwargs)


def info(*args: Any, **kwargs: Any) -> None:
    """Logger for info category."""
    print('[INFO]', *args, **kwargs)


def warn(*args: Any, **kwargs: Any) -> None:
    """Logger for warn category."""
    print('[WARN]', *args, **kwargs)


def warning(*args: Any, **kwargs: Any) -> None:
    """Logger for warn category."""
    print('[WARNING]', *args, **kwargs)


def error(*args: Any, **kwargs: Any) -> None:
    """Logger for error category."""
    print('[ERROR]', *args, **kwargs)
