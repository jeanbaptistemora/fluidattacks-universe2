from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Iterator,
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def get_argument(graph: Graph, nid: NId, expected_block: str) -> Optional[str]:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        name = graph.nodes[block_id].get("name")
        if name == expected_block:
            return block_id
    return None


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


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> Tuple[Optional[str], str]:
    for attr_id in adj_ast(graph, object_id, label_type="Pair"):
        key, value = get_key_value(graph, attr_id)
        if key == expected_attr:
            return key, value
    return None, ""


def iterate_resource(graph: Graph, expected_resource: str) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        name = graph.nodes[nid].get("name")
        if name and name == expected_resource:
            yield nid
