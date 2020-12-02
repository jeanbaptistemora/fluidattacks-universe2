# Standard library
from typing import (
    Any,
    Callable,
)

# Third party libraries
import networkx as nx

# Local libraries
from eval_java.model import (
    Context,
    OptionalContext,
)
from utils.function import (
    get_id,
)
from utils.logs import (
    blocking_log,
)


def mark_seen(ctx: Context, n_id: str) -> Context:
    ctx['seen'].add(n_id)

    return ctx


def ensure_context(ctx: OptionalContext = None) -> Context:
    if ctx is None:
        return {
            'complete': True,
            'seen': set(),
            'statements': [],
        }

    return ctx


def mark_if_sink(graph: nx.DiGraph, n_id: str, ctx: Context) -> None:
    if statements := ctx['statements']:
        if label := graph.nodes[n_id].get('label_sink_type'):
            statements[-1]['sink'] = label


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
