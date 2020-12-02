# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementLiteral,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    ctx.statements.append(StatementLiteral(
        meta=get_default_statement_meta(),
        value=graph.nodes[n_id]['label_text'],
    ))

    return common.mark_seen(ctx, n_id)
