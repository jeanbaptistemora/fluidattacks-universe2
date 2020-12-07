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
    StatementAdd,
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

    match = g.match_ast(graph, n_id, '__0__', 'ADD', '__1__')

    if (
        match['ADD']
        and (left_id := match.get('__0__'))
        and (right_id := match.get('__1__'))
    ):
        l_ctx = generic.evaluate(graph, left_id, ctx=None)
        r_ctx = generic.evaluate(graph, right_id, ctx=None)
        common.merge_contexts(ctx, l_ctx)
        common.merge_contexts(ctx, r_ctx)

        ctx.statements.append(StatementAdd(
            meta=get_default_statement_meta(),
            stacks=[
                r_ctx.statements,
                l_ctx.statements,
            ],
        ))
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
