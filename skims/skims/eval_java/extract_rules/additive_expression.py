# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    StatementAdd,
    OptionalContext,
)
from model import (
    graph_model,
)
from utils import (
    graph as g,
)


def extract(
    graph: graph_model.Graph,
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
        l_ctx = generic.extract(graph, left_id, ctx=None)
        r_ctx = generic.extract(graph, right_id, ctx=None)
        common.merge_contexts(ctx, l_ctx)
        common.merge_contexts(ctx, r_ctx)

        ctx.statements.append(StatementAdd(
            meta=get_default_statement_meta(),
            sign=common.translate_match(graph, op_id, {
                'ADD': '+',
                'SUB': '-',
            }),
            stacks=[
                r_ctx.statements,
                l_ctx.statements,
            ],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
