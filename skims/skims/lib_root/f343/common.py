from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def webpack_insecure_compression(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in g.matching_nodes(graph, label_type="placeholder"):
        vuln_nodes.add(n_id)
    return vuln_nodes
