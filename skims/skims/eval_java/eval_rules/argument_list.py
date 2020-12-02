# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    OptionalContext,
)
from utils import (
    graph as g,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    for c_id in g.adj_ast(graph, n_id):
        c_attrs_label_type = graph.nodes[c_id]['label_type']

        if c_attrs_label_type != 'COMMA':
            c_ctx = generic.evaluate(graph, c_id, ctx=None)
            common.merge_contexts(ctx, c_ctx)
            ctx.statements.extend(c_ctx.statements)

    return common.mark_seen(ctx, n_id)
