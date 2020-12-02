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

    match = g.match_ast(
        graph,
        n_id,
        'NEW',
        'CustomIdentifier',
        'LPAREN',
        'RPAREN',
    )

    if (
        match['NEW']
        and match['CustomIdentifier']
        and match['LPAREN']
        and (arg_id := match['__0__'])
        and match['RPAREN']
    ):
        args_ctx = generic.evaluate(graph, arg_id, ctx=None)
        common.merge_contexts(ctx, args_ctx)
        args = args_ctx['statements']

        ctx['statements'].append({
            'stack': args,
            'class_type': graph.nodes[match['CustomIdentifier']]['label_text'],
            'type': 'CLASS_INSTANTIATION',
        })
        common.mark_if_sink(graph, n_id, ctx)
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
