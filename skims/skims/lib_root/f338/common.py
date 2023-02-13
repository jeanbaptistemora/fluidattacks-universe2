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


def has_dangerous_param(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    sensitive_methods = {"salt"}

    for n_id in g.matching_nodes(graph, label_type="VariableDeclaration"):
        if graph.nodes[n_id].get("variable") in sensitive_methods:
            child = g.adj_ast(graph, n_id)[0]
            if (
                graph.nodes[child].get("value_type") == "string"
                and graph.nodes[child].get("label_type") == "Literal"
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
