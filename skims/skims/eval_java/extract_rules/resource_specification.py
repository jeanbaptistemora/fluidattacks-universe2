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


def extract(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(graph, n_id, 'Resource', 'ResourceList')

    if c_id := match['Resource']:
        _resource(graph, c_id, ctx=ctx)
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)


def _resource(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(
        graph,
        n_id,
        '__0__',
        '__1__',
        'ASSIGN',
        '__2__',
    )

    if (
        (type_id := match['__0__'])
        and (var_id := match['__1__'])
        and match['ASSIGN']
        and (src_id := match['__2__'])
    ):
        src_ctx = generic.extract(graph, src_id, ctx=None)
        common.merge_contexts(ctx, src_ctx)

        var_attrs = graph.nodes[var_id]
        type_attrs = graph.nodes[type_id]

        # Add the variable to the mapping
        ctx.statements.append(StatementDeclaration(
            meta=get_default_statement_meta(),
            stack=src_ctx.statements,
            var=var_attrs['label_text'],
            var_type=type_attrs['label_text'],
        ))
    else:
        common.not_implemented(extract, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
