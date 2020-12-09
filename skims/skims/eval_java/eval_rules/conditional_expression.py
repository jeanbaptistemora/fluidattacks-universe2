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
    ExpressionConditional,
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

    match = g.match_ast(
        graph, n_id,
        '__0__',
        'QUESTION',
        '__1__',
        'COLON',
        '__2__',
    )

    if (
        (pred_id := match['__0__'])
        and match['QUESTION']
        and (true_id := match['__1__'])
        and match['COLON']
        and (false_id := match['__2__'])
    ):
        pred_ctx = generic.evaluate(graph, pred_id, ctx=None)
        common.merge_contexts(ctx, pred_ctx)
        true_ctx = generic.evaluate(graph, true_id, ctx=None)
        common.merge_contexts(ctx, true_ctx)
        false_ctx = generic.evaluate(graph, false_id, ctx=None)
        common.merge_contexts(ctx, false_ctx)

        ctx.statements.append(ExpressionConditional(
            meta=get_default_statement_meta(),
            stacks=[
                pred_ctx.statements,
                true_ctx.statements,
                false_ctx.statements,
            ],
        ))
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
