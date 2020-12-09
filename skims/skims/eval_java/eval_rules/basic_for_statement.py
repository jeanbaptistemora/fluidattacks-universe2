# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
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

    # for (int i = 0; i < 10; i++) {...}
    types = (
        'FOR',
        'LPAREN',
        'LocalVariableDeclaration',
        'RPAREN',
        'Block',
    )
    for_update = (
        'PreIncrementExpression',
        'PreDecrementExpression',
        'PostIncrementExpression',
        'PostDecrementExpression',
    )
    match = g.match_ast(graph, n_id, *types, *for_update)

    if (
        match['FOR']  # pylint: disable=too-many-boolean-expressions
        and match['LPAREN']
        and match['LocalVariableDeclaration']
        and any(match.get(expression) for expression in for_update)
        and match['RPAREN']
        and match['Block']
    ):
        # evaluate LocalVariableDeclaration
        src_ctx = generic.local_variable_declaration_statement.evaluate(
            graph,
            n_id,
            ctx=None,
        )
        common.merge_contexts(ctx, src_ctx)
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
