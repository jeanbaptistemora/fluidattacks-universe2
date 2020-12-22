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
        # Please remove this line if you want to see the traces
        #   it's hidden in normal operations to avoid cluttering logs
        log_to=None,
        overridden_function=overridden_function,
    )
