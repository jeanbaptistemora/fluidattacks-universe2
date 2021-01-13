# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    ExpressionBinary,
)
from utils import (
    graph as g,
)
from model.graph_model import (
    Graph,
)


def extract(
    graph: Graph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(graph, n_id, '__0__', '__1__', '__2__')

    if (
        len(match) == 3
        and (left_id := match['__0__'])
        and (op_id := match['__1__'])
        and (right_id := match['__2__'])
    ):
        left_ctx = generic.extract(graph, left_id, ctx=None)
        common.merge_contexts(ctx, left_ctx)
        right_ctx = generic.extract(graph, right_id, ctx=None)
        common.merge_contexts(ctx, right_ctx)

        ctx.statements.append(ExpressionBinary(
            meta=get_default_statement_meta(),
            operator=common.translate_match(graph, op_id, {
                'AND': '&&',
            }),
            stacks=[
                left_ctx.statements,
                right_ctx.statements,
            ],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
