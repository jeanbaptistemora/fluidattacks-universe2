# Standard library
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
)

# Local libraries
from utils.function import (
    get_id,
)
from utils.logs import (
    blocking_log,
)

# Types
Context = Dict[str, Dict[str, Any]]
OptionalContext = Optional[Context]


def _build_empty_context() -> Context:
    ctx: Context = {
        'inputs': {
            'vars': {},
        },
        'vars': {},
    }

    return ctx


def ensure_context(ctx: OptionalContext) -> Context:
    return _build_empty_context() if ctx is None else ctx


def warn_not_impl(function: Callable[..., Any], **kwargs: Any) -> None:
    blocking_log(
        'warning',
        'Missing case handling in %s: %s',
        get_id(function),
        kwargs,
    )
