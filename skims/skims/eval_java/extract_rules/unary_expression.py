# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    ExpressionUnary,
    get_default_statement_meta,
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
    return common.extract_until_handled(
        graph,
        n_id,
        ctx=ctx,
        extract=extract,
        evaluators=(
            _extract_case_1,
        )
    )


def _extract_case_1(
    graph: graph_model.Graph,
    n_id: str,
    *,
    ctx: Context,
) -> Context:
    match = g.match_ast(graph, n_id, 'BANG', '__0__')

    # pylint: disable=used-before-assignment
    if (
        len(match) == 2
        and match['BANG']
        and (c_id := match['__0__'])
    ):
        c_ctx = generic.extract(graph, c_id, ctx=None)
        common.merge_contexts(ctx, c_ctx)

        ctx.statements.append(ExpressionUnary(
            meta=get_default_statement_meta(),
            operator='!',
            stack=c_ctx.statements,
        ))
        common.mark_if_sink(graph, n_id, ctx)
    else:
        raise common.NotHandled()

    return ctx
