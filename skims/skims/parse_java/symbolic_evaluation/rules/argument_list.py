# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)
from parse_java.symbolic_evaluation.rules import (
    generic,
)
from utils import (
    graph as g,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    for c_id in g.adj_ast(graph, n_id):
        c_attrs_label_type = graph.nodes[c_id]['label_type']

        if c_attrs_label_type != 'COMMA':
            c_ctx = generic.evaluate(graph, c_id, ctx=None)
            common.merge_contexts(ctx, c_ctx)
            ctx['log'].extend(c_ctx['log'])

    return common.mark_seen(ctx, n_id)
