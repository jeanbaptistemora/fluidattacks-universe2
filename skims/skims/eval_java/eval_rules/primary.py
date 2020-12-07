# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementPrimary,
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

    statement_ids = g.adj_ast(graph, n_id)
    context_statements = []
    for s_id in statement_ids:
        n_ctx = generic.evaluate(graph, s_id, ctx=None)
        common.merge_contexts(ctx, n_ctx)
        context_statements.append(n_ctx.statements)

    ctx.statements.append(StatementPrimary(
        meta=get_default_statement_meta(),
        stacks=context_statements,
    ))

    return common.mark_seen(ctx, n_id)
