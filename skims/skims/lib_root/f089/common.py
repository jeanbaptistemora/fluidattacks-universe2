from model.graph_model import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def json_parse_unval_data(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_expressions: set[str] = {
        "localStorage.getItem",
        "sessionStorage.getItem",
    }
    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="JSON.parse"
    ):
        for m_id in g.get_nodes_by_path(
            graph, n_id, [], "ArgumentList", "MethodInvocation"
        ):
            if (exp := graph.nodes[m_id].get("expression")) and (
                exp in danger_expressions
            ):
                vuln_nodes.append(n_id)
    return vuln_nodes
