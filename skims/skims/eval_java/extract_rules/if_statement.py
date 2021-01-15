# Local libraries
from eval_java.extract_rules import (
    common,
    generic,
)
from eval_java.model import (
    Context,
    get_default_statement_meta,
    StatementIf,
    OptionalContext,
)
from utils import (
    graph as g,
)
from model import (
    graph_model,
)


def extract(
    graph: graph_model.Graph,
    n_id: str,
    *,
    ctx: OptionalContext,
) -> Context:
    ctx = common.ensure_context(ctx)

    predicate_id = g.adj_ast(graph, n_id)[2]
    predicate_ctx = generic.extract(graph, predicate_id, ctx=None)
    common.merge_contexts(ctx, predicate_ctx)

    ctx.statements.append(StatementIf(
        cfg_condition=g.get_node_cfg_condition(graph, ctx.path_edges[n_id]),
        meta=get_default_statement_meta(),
        stack=predicate_ctx.statements,
    ))

    return common.mark_seen(ctx, n_id)
