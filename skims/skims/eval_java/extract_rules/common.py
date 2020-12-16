# Standard library
from typing import (
    Any,
    Callable,
    Dict,
    Tuple,
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


class NotHandled(Exception):
    pass


def mark_seen(ctx: Context, n_id: str) -> Context:
    ctx.seen.add(n_id)

    return ctx


def ensure_context(ctx: OptionalContext = None) -> Context:
    if ctx is None:
        return Context(
            complete=True,
            path_edges={},
            seen=set(),
            statements=[],
        )

    return ctx


def extract_until_handled(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
    extract: Callable[..., Context],
    evaluators: Tuple[Callable[..., Context], ...],
) -> Context:
    ctx = ensure_context(ctx)

    for evaluator in evaluators:
        try:
            ctx = evaluator(graph, n_id, ctx=ctx)
        except NotHandled:
            continue
        else:
            break
    else:
        not_implemented(extract, n_id, ctx=ctx)

    return mark_seen(ctx, n_id)


def mark_if_sink(graph: nx.DiGraph, n_id: str, ctx: Context) -> None:
    if statements := ctx.statements:
        if label := graph.nodes[n_id].get('label_sink_type'):
            statements[-1].meta.sink = label


def merge_contexts(target: Context, source: Context) -> None:
    target.seen.update(source.seen)


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

    ctx.complete = False


def translate_match(
    graph: nx.DiGraph,
    op_id: str,
    translations: Dict[str, str],
) -> str:
    for key, val in translations.items():
        if graph.nodes[op_id]['label_type'] == key:
            return val

    raise NotImplementedError()
