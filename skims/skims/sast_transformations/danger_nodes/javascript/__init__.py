from model.graph_model import (
    Graph,
    GraphSyntax,
)
from sast_transformations.danger_nodes.javascript import (
    express,
)


def mark_inputs(
    graph: Graph,
    syntax: GraphSyntax,
) -> None:
    express.mark_requests(graph, syntax)
