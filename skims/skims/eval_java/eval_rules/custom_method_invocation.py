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
            args = args_ctx['statements']
        else:
            args = []

        ctx['statements'].append({
            'stack': args,
            'method': method,
            'type': 'CALL',
        })
    else:
        common.not_implemented(evaluate, n_id, ctx=ctx)

    return common.mark_seen(ctx, n_id)
