"""Mark graph nodes as sinks and map them to a vulnerability type."""

# Standard library
from typing import (
    Set,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)

# Constants
SINKS: Set[str] = {
    'F063_PATH_TRAVERSAL',
}


def _path_traversal(graph: nx.DiGraph) -> None:
    # Class instantiations of given type
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CustomClassInstanceCreationExpression_lfno_primary',
    )):
        pattern = ('NEW', 'CustomIdentifier', 'LPAREN', '__0__', 'RPAREN')
        match = g.match_ast(graph, n_id, *pattern)

        # Filter childs of CustomIdentifier type
        if (
            match['NEW']
            and (c_id := match['CustomIdentifier'])
            and match['LPAREN']
            and match['RPAREN']
            and graph.nodes[c_id]['label_text'] in {
                'java.io.File',
                'io.File',
                'File',

                'java.io.FileOutputStream',
                'io.FileOutputStream',
                'FileOutputStream',
            }
        ):
            graph.nodes[n_id]['label_sink_type'] = 'F063_PATH_TRAVERSAL'


def _insecure_randoms(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='CustomMethodInvocation_lfno_primary',
    )):
        if g.filter_nodes(
            graph,
            nodes=g.adj(graph, n_id),
            predicate=lambda n_attrs: n_attrs['label_type'] ==
            'CustomIdentifier' and n_attrs['label_text'].endswith(
                'getSession'),
        ):
            m_invocation = g.pred_ast(graph, n_id)[0]
            if graph.nodes[m_invocation][
                    'label_type'] == 'CustomMethodInvocation':
                if g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, m_invocation),
                    predicate=lambda n_attrs: n_attrs['label_type'] ==
                    'CustomIdentifier' and n_attrs['label_text'].endswith(
                        'setAttribute'),
                ):
                    graph.nodes[m_invocation][
                        'label_sink_type'] = 'F034_INSECURE_RANDOMS'


def mark(graph: nx.DiGraph) -> None:
    _path_traversal(graph)
    _insecure_randoms(graph)
