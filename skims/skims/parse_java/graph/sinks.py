"""Mark graph nodes as sinks and map them to a vulnerability type."""

# Standard library
from itertools import (
    chain,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def _path_traversal(graph: nx.DiGraph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='ClassInstanceCreationExpression_lfno_primary',
    )):
        # Filter childs of CustomIdentifier type
        for _ in chain.from_iterable(
            g.filter_nodes(
                graph,
                nodes=g.adj(graph, n_id),
                predicate=g.pred_has_labels(
                    label_type='CustomIdentifier',
                    label_text=label_text,
                ),
            )
            for label_text in ('java.io.File', 'io.File', 'File')
        ):
            graph.nodes[n_id]['label_sink_type'] = 'F063_PATH_TRAVERSAL'
            break


def mark(graph: nx.DiGraph) -> None:
    _path_traversal(graph)
