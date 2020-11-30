# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    ctx['statements'].append({
        'value':  graph.nodes[n_id]['label_text'],
        'type': 'LITERAL',
    })

    return common.mark_seen(ctx, n_id)
