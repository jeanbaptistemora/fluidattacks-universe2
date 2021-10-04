from context import (
    FI_DEBUG as DEBUG,
)
import tracers.function
from typing import (
    Any,
    Callable,
    Optional,
)


def trace(overridden_function: Optional[Callable[..., Any]] = None) -> Any:
    # pylint: disable=unsubscriptable-object
    return tracers.function.trace(
        enabled=DEBUG.lower() == "true",
        # Please remove this line if you want to see the traces
        #   it's hidden in normal operations to avoid cluttering logs
        log_to=None,
        overridden_function=overridden_function,
    )
