# Local libraries
from eval_java.extract_rules import (
    common,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementLookup,
)
from model import (
    graph_model,
)


def extract(
    graph: graph_model.Graph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    ctx.statements.append(StatementLookup(
        meta=get_default_statement_meta(),
        symbol=graph.nodes[n_id]['label_text'],
    ))

    return common.mark_seen(ctx, n_id)
