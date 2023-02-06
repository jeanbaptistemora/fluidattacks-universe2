from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Iterator,
    Tuple,
)
from utils import (
    graph as g,
)


def get_key_value(graph: Graph, nid: NId) -> Tuple[str, str]:
    key_id = graph.nodes[nid]["key_id"]
    key = graph.nodes[key_id]["value"]
    value_id = graph.nodes[nid]["value_id"]
    value = (
        graph.nodes[value_id]["value"]
        if graph.nodes[value_id].get("value")
        else ""
    )
    return key, value


def iterate_resource(graph: Graph, expected_resource: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        name = graph.nodes[nid].get("name")
        if name and name == expected_resource:
            yield nid
