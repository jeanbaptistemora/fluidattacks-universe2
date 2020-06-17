# Standard library
from typing import (
    Callable,
)

# Third party libraries
import tracers.function

# Local libraries
from __init__ import (
    FI_DEBUG as DEBUG,
)


def trace(display_name: str = '') -> Callable:
    return tracers.function.trace(
        do_trace=DEBUG.lower() == 'true',
        function_name=display_name,
    )
