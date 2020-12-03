"""Modify in-place sub-trees of the graph in order to simplify it."""

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def _mark_methods(graph: nx.DiGraph) -> None:
    for n_attrs in graph.nodes.values():
        if n_attrs['label_type'] == 'MethodDeclaration':
            n_attrs['label_input_type'] = 'function'


def _mark_randoms(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CustomClassInstanceCreationExpression_lfno_primary',
    )):
        if g.filter_nodes(
            graph,
            nodes=g.adj(graph, n_id),
            predicate=lambda n_attrs: n_attrs['label_type'] ==
            'CustomIdentifier' and n_attrs['label_text'] in {
                'java.util.Random',
                'util.Random',
                'Random',
            },
        ):

            for parent in g.pred_ast_lazy(graph, n_id, depth=-1):
                if graph.nodes[parent]['label_type'].endswith('Statement'):
                    graph.nodes[parent]['label_input_type'] = 'insecure_random'
                    break


def mark(graph: nx.DiGraph) -> None:
    _mark_methods(graph)
    _mark_randoms(graph)
