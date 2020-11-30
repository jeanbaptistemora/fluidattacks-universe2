# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
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

    for c_id in g.adj(graph, n_id):
        c_ctx = generic.inspect(graph, c_id, ctx=None)
        common.merge_contexts(ctx, c_ctx)

        ctx['log'].extend(c_ctx['log'])

    return common.mark_seen(ctx, n_id)
