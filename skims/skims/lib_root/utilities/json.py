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
