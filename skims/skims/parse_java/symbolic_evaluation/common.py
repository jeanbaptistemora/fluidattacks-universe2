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
Context = Dict[str, Any]
OptionalContext = Optional[Context]


def _build_empty_context() -> Context:
    ctx: Context = {
        'complete': True,
        'seen': set(),
        'statements': [],
    }

    return ctx


def already_seen(ctx: Context, n_id: str) -> bool:
    return n_id in ctx['seen']


def mark_seen(ctx: Context, n_id: str) -> Context:
    ctx['seen'].add(n_id)

    return ctx


def ensure_context(ctx: OptionalContext) -> Context:
    return _build_empty_context() if ctx is None else ctx


def merge_contexts(target: Context, source: Context) -> None:
    target['seen'].update(source['seen'])


def not_implemented(
    function: Callable[..., Any],
    n_id: str,
    *,
    ctx: Context
) -> None:
    blocking_log(
        'debug',
        'Missing case handling in %s: %s',
        get_id(function),
        n_id,
    )

    ctx['complete'] = False
