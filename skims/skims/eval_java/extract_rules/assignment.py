# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    OptionalContext,
    StatementAssignment,
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

    # variableDeclaratorId ('=' variableInitializer)?
    assigns = {
        'ASSIGN',
        'ADD_ASSIGN',
        'SUB_ASSIGN',
        'MUL_ASSIGN',
        'DIV_ASSIGN',
        'AND_ASSIGN',
        'OR_ASSIGN',
        'XOR_ASSIGN',
        'MOD_ASSIGN',
        'LSHIFT_ASSIGN',
        'RSHIFT_ASSIGN',
        'URSHIFT_ASSIGN',
    }
    match = g.match_ast(
        graph,
        n_id,
        'IdentifierRule',
        '__0__',
        *assigns,
    )
    if (
        match['IdentifierRule']
        and any(match.get(assign) for assign in assigns)
        and (src_id := match['__0__'])
    ):
        src_ctx = generic.extract(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        # Add the variable to the mapping
        ctx.statements.append(StatementAssignment(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            var=graph.nodes[match['IdentifierRule']]['label_text'],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
