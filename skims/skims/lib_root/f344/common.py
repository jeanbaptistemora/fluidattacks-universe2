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


def is_vuln(graph: Graph, n_id: NId) -> bool:
    for m_id in g.matching_nodes(graph, label_type="PlaceHolder"):
        if m_id == n_id:
            return True
    return False


def local_storage_from_http(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="localStorage.setItem"
    ):
        if (
            (parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList"))
            and (value_n_id := g.adj(graph, parameters_n_id)[1])
            and is_vuln(graph, value_n_id)
        ):
            vuln_nodes.add(n_id)
    return vuln_nodes
