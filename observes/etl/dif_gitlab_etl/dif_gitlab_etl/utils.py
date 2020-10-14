# Standard libraries
import sys
# Third party libraries
# Local libraries


def log(level: str, msg: str) -> None:
    """Print information to the console labeled with `level`"""
    print(f'[{level.upper()}]', msg, file=sys.stderr, flush=True)


def error(msg: str) -> None:
    """Handle and raise a custom error message."""
    raise Exception(msg)
