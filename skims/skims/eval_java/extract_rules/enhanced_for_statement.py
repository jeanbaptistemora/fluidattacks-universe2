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
    StatementDeclaration,
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

    # for (Cookie cookie : cookies) {...}
    types = (
        'FOR',
        'LPAREN',
        'CustomUnannClassOrInterfaceType',
        'IdentifierRule',
        'COLON',
        '__0__',
        'RPAREN',
    )
    match = g.match_ast(graph, n_id, *types)

    if (
        match['FOR']  # pylint: disable=too-many-boolean-expressions
        and match['LPAREN']
        and (var_type := match['CustomUnannClassOrInterfaceType'])
        and (var := match['IdentifierRule'])
        and match['COLON']
        and (src := match['__0__'])
        and match['RPAREN']
    ):
        src_ctx = generic.evaluate(graph, src, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        # Add the variable to the mapping
        ctx.statements.append(StatementDeclaration(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            var=graph.nodes[var]['label_text'],
            var_type=graph.nodes[var_type]['label_text'],
        ))
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
