from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def iterate_resource(graph: Graph, expected_resource: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        name = graph.nodes[nid].get("name")
        if name and name == expected_resource:
            yield nid
