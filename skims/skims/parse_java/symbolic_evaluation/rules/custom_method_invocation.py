# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)
from parse_java.symbolic_evaluation.rules import (
    generic,
)
from utils import (
    graph as g,
)


def evaluate(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
    ctx = common.ensure_context(ctx)

    match = g.match_ast(
        graph,
        n_id,
        'CustomIdentifier',
        'LPAREN',
        '__0__',
        'RPAREN',
    )

    if (
        match['CustomIdentifier']
        and match['LPAREN']
        and match['RPAREN']
    ):
        method = graph.nodes[match['CustomIdentifier']]['label_text']

        if args_id := match['__0__']:
            args_ctx = generic.evaluate(graph, args_id, ctx=None)
            common.merge_contexts(ctx, args_ctx)
            args = args_ctx['log']
        else:
            args = []

        ctx['log'].append({
            'args': args,
            'method': method,
            'type': 'CALL',
        })
    else:
        common.warn_not_impl(evaluate, n_id=n_id)

    return common.mark_seen(ctx, n_id)
