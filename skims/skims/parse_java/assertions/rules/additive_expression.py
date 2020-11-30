# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
)
from parse_java.assertions.rules import (
    generic,
)
from utils import (
    graph as g,
)


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(graph, n_id, '__0__', 'ADD', '__1__')

    if (
        match['ADD']
        and (left_id := match['__0__'])
        and (right_id := match['__1__'])
    ):
        l_ctx = generic.inspect(graph, left_id, ctx=None)
        r_ctx = generic.inspect(graph, right_id, ctx=None)
        common.merge_contexts(ctx, l_ctx)
        common.merge_contexts(ctx, r_ctx)

        ctx['log'].append({
            'left': l_ctx['log'],
            'right': r_ctx['log'],
            'type': 'ADD',
        })
    else:
        common.warn_not_impl(inspect, n_id=n_id)

    return common.mark_seen(ctx, n_id)
