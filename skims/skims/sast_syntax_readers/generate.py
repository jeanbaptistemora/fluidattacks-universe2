from __future__ import (
    annotations,
)

from model import (
    graph_model,
)


def read_from_graph(
    graph: graph_model.Graph,
) -> graph_model.GraphSyntax:
    graph_syntax: graph_model.GraphSyntax = {}
    # Read the syntax of every node in the graph, if possible
    for n_id in graph.nodes:
        if n_id not in graph_syntax:
            graph_syntax[n_id] = [n_id]
    return graph_syntax
