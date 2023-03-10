from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def unsafe_xss_content_nodes(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_set = {"userconnection"}

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        n_attrs = graph.nodes[n_id]
        m_name = n_attrs["expression"].split(".")[-1]
        expr_id = n_attrs["expression_id"]
        if (
            m_name == "send"
            and graph.nodes[expr_id]["label_type"] == "MemberAccess"
            and graph.nodes[expr_id]["member"] in {"res", "response"}
        ):
            al_id = graph.nodes[n_id].get("arguments_id")
            if (
                al_id
                and (args_ids := g.adj_ast(graph, al_id))
                and len(args_ids) == 1
                and get_node_evaluation_results(
                    method, graph, args_ids[0], danger_set
                )
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
