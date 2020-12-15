# Third party libraries
import networkx as nx

# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    ExpressionRelational,
)
from utils import (
    graph as g,
)


def extract(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(graph, n_id, '__0__', '__1__', '__2__')

    # pylint: disable=used-before-assignment
    if (
        len(match) == 3
        and (left_id := match['__0__'])
        and (op_id := match['__1__'])
        and graph.nodes[op_id]['label_type'] in {
            'GE',
            'GT',
            'INSTANCEOF',
            'LE',
            'LT',
        }
        and (right_id := match['__2__'])
    ):
        left_ctx = generic.extract(graph, left_id, ctx=None)
        common.merge_contexts(ctx, left_ctx)
        right_ctx = generic.extract(graph, right_id, ctx=None)
        common.merge_contexts(ctx, right_ctx)

        ctx.statements.append(ExpressionRelational(
            meta=get_default_statement_meta(),
            operator=graph.nodes[op_id]['label_text'],
            stacks=[
                left_ctx.statements,
                right_ctx.statements,
            ],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
