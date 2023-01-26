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


def json_parse_unval_data(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.matching_nodes(graph, label_type="Placeholder"):
        vuln_nodes.append(n_id)
    return vuln_nodes
