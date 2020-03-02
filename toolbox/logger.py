# Local imports
from toolbox import constants


def debug(*args, **kwargs):
    """Logger for debug category."""
    if constants.LOGGER_DEBUG:
        print('[DEBUG]', *args, **kwargs)


def info(*args, **kwargs):
    """Logger for info category."""
    print('[INFO]', *args, **kwargs)


def warn(*args, **kwargs):
    """Logger for warn category."""
    print('[WARNING] ', *args, **kwargs)


def error(*args, **kwargs):
    """Logger for error category."""
    print('[ERROR]', *args, **kwargs)
