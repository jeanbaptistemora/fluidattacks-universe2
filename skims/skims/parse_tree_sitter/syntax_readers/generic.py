# Standard library

# Local libraries
from typing import (
    Callable,
    Set,
    Tuple,
)
from model import (
    graph_model,
)

# Constants
READERS: Tuple[
    Tuple[
        Set[str],
        Callable[
            [graph_model.Graph, graph_model.NId],
            graph_model.SyntaxSteps,
        ],
    ],
    ...,
] = (
)


def read_from_graph(
    graph: graph_model.Graph,
) -> graph_model.GraphSyntax:
    graph_syntax: graph_model.GraphSyntax = {}

    for n_id, n_attrs in graph.nodes.items():
        graph_syntax[n_id] = []

        for label_types, reader in READERS:
            if n_attrs['label_type'] in label_types:
                syntax = reader(graph, n_id)

                graph_syntax[n_id] = syntax

    return graph_syntax
