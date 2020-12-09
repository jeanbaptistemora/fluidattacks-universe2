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
    StatementClassInstantiation,
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
        graph,
        n_id,
        'NEW',
        '__0__',
        'LPAREN',
        '__1__',
        'RPAREN',
    )

    # pylint: disable=too-many-boolean-expressions
    # pylint: disable=used-before-assignment
    if (
        match['NEW']
        and (class_type_id := match['__0__'])
        and match['LPAREN']
        and (arg_id := match['__1__'])
        and match['RPAREN']
        and graph.nodes[class_type_id]['label_type'] in {
            'CustomIdentifier',
            'IdentifierRule',
        }
    ):
        args = []
        if arg_id:
            args_ctx = generic.evaluate(graph, arg_id, ctx=None)
            common.merge_contexts(ctx, args_ctx)
            args = args_ctx.statements

        ctx.statements.append(StatementClassInstantiation(
            class_type=graph.nodes[class_type_id]['label_text'],
            meta=get_default_statement_meta(),
            stack=args,
        ))
        common.mark_if_sink(graph, n_id, ctx)
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
