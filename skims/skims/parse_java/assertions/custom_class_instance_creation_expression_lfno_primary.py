# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
    generic,
)
from utils import (
    graph as g,
)


def inspect(
    graph: nx.DiGraph,
    n_id: str,
    *,
    ctx: common.OptionalContext,
) -> common.Context:
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
        arg_attrs_label_type = graph.nodes[arg_id]['label_type']

        if arg_attrs_label_type == 'IdentifierRule':
            args = [{
                'symbol': graph.nodes[arg_id]['label_text'],
                'type': 'LOOKUP',
            }]
        else:
            args_ctx = generic.inspect(graph, arg_id, ctx=None)
            common.merge_contexts(ctx, args_ctx)
            args = args_ctx['log']

        ctx['log'].append({
            'args': args,
            'class_type': graph.nodes[match['CustomIdentifier']]['label_text'],
            'type': 'CLASS_INSTANTIATION',
        })
    else:
        common.warn_not_impl(inspect, n_id=n_id)

    return common.mark_seen(ctx, n_id)
