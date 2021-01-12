# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementCast,
)
from utils import (
    graph as g,
)
from utils.model import (
    Graph,
)


def extract(
    graph: Graph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(
        graph, n_id,
        'LPAREN',
        'IdentifierRule',
        'RPAREN',
        '__0__',
    )

    if (
        match['LPAREN']
        and (class_type_id := match['IdentifierRule'])
        and match['RPAREN']
        and (src_id := match['__0__'])
    ):
        src_ctx = generic.extract(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        ctx.statements.append(StatementCast(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            class_type=graph.nodes[class_type_id]['label_text'],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
