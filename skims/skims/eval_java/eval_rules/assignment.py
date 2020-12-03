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
    StatementAssignment,
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

    # variableDeclaratorId ('=' variableInitializer)?
    match = g.match_ast(graph, n_id, 'IdentifierRule', 'ASSIGN', '__0__')

    if (
        match['IdentifierRule']
        and match['ASSIGN']
        and (src_id := match['__0__'])
    ):
        src_ctx = generic.evaluate(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        # Add the variable to the mapping
        ctx.statements.append(StatementAssignment(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            var=graph.nodes[match['IdentifierRule']]['label_text'],
        ))
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
