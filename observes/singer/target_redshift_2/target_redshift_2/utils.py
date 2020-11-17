# Standard libraries
import sys
from typing import Callable, TypeVar
# Third party libraries
# Local libraries
DEBUG_ENABLED = True

Source = TypeVar("Source")
Target = TypeVar("Target")
Transform = Callable[[Source], Target]


def log(level: str, msg: str) -> None:
    """Print information to the console labeled with `level`"""
    u_level = level.upper()
    if u_level == 'DEBUG' and not DEBUG_ENABLED:
        return
    print(f'[{u_level}]', msg, file=sys.stderr, flush=True)
