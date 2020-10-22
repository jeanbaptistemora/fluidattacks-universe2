# Standard libraries
import sys
# Third party libraries
# Local libraries
DEBUG_ENABLED = True


def log(level: str, msg: str) -> None:
    """Print information to the console labeled with `level`"""
    u_level = level.upper()
    if u_level == 'DEBUG' and not DEBUG_ENABLED:
        return
    print(f'[{u_level}]', msg, file=sys.stderr, flush=True)


def error(msg: str) -> None:
    """Handle and raise a custom error message."""
    raise Exception(msg)


class NotFoundException(Exception):
    def __init__(self, msg):
        log('exception', 'NotFound: ' + msg)
        super().__init__(msg)
