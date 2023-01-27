from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def get_value(graph: Graph, nid: NId) -> str:
    value = graph.nodes[nid]["value"] if graph.nodes[nid].get("value") else ""
    return value


def is_parent(graph: Graph, nid: NId, parents: List[str]) -> bool:
    last_nid = nid
    for correct_parent in parents:
        parent = g.search_pred_until_type(graph, last_nid, {"Pair"})
        parent_id = parent[0] if parent != ("", "") else None
        if parent_id:
            key_id = graph.nodes[parent_id]["key_id"]
            key = graph.nodes[key_id]["value"]
            if key == correct_parent:
                last_nid = parent_id
                continue
            return False
        return False
    return True


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False
