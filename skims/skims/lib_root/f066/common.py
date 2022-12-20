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


def nid_uses_console_log(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        if graph.nodes[n_id].get("expression") == "console.log":
            vuln_nodes.append(n_id)
    return vuln_nodes
