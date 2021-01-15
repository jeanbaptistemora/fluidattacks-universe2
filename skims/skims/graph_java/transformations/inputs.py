"""Modify in-place sub-trees of the graph in order to simplify it."""

# Third party libraries
from typing import (
    Optional,
)

# Local libraries
from model import (
    graph_model,
)
from utils import (
    graph as g,
)


def _search_parent_statement(
    graph: graph_model.Graph,
    n_id: str,
) -> Optional[str]:
    for parent in g.pred_ast_lazy(graph, n_id, depth=-1):
        if graph.nodes[parent]['label_type'].endswith('Statement'):
            return parent
    return None


def _mark_methods(graph: graph_model.Graph) -> None:
    for n_attrs in graph.nodes.values():
        if n_attrs['label_type'] == 'MethodDeclaration':
            n_attrs['label_input_type'] = 'function'


def _mark_randoms(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CustomClassInstanceCreationExpression_lfno_primary',
    )):
        pattern_util = ('NEW', 'CustomIdentifier', 'LPAREN', 'RPAREN')
        match = g.match_ast(graph, n_id, *pattern_util)

        if (
            match['NEW']
            and (c_id := match['CustomIdentifier'])
            and match['LPAREN']
            and match['RPAREN']
            and graph.nodes[c_id]['label_text'] in {
                'java.util.Random',
                'util.Random',
                'Random',
            }
        ):
            if parent := _search_parent_statement(graph, n_id):
                graph.nodes[parent]['label_input_type'] = 'insecure_random'

    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CustomMethodInvocation_lfno_primary',
    )):
        pattern_math = ('CustomIdentifier', 'LPAREN', 'RPAREN')
        match = g.match_ast(graph, n_id, *pattern_math)
        if (
            (c_id := match['CustomIdentifier'])
            and match['LPAREN']
            and match['RPAREN']
            and graph.nodes[c_id]['label_text'] in {
                'java.lang.Math.random',
                'lang.Math.random',
                'Math.random',
                'random',
            }
        ):
            if parent := _search_parent_statement(graph, n_id):
                graph.nodes[parent]['label_input_type'] = 'insecure_random'


def mark(graph: graph_model.Graph) -> None:
    _mark_methods(graph)
    _mark_randoms(graph)
