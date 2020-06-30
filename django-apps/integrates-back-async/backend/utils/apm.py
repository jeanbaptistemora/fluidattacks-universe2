# Standard library
from typing import (
    Callable,
    Optional,
)

# Third party libraries
import tracers.function

# Local libraries
from __init__ import (
    FI_DEBUG as DEBUG,
)


def trace(overridden_function: Optional[Callable] = None) -> Callable:
    return tracers.function.trace(
        enabled=DEBUG.lower() == 'true',
        overridden_function=overridden_function,
    )
