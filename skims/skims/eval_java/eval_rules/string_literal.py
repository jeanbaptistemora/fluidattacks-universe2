# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
)
from eval_java.model import (
    Context,
    OptionalContext,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    ctx['statements'].append({
        'value':  graph.nodes[n_id]['label_text'],
        'type': 'LITERAL',
    })

    return common.mark_seen(ctx, n_id)
