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


def is_insecure_param(
    method: MethodsEnum,
    graph: Graph,
    al_id: NId,
) -> bool:
    danger_types = {"Object", "SymbolLookup"}
    rules = {"InsecureCookie"}
    args_ids = g.adj_ast(graph, al_id)
    for p_id in args_ids:
        if graph.nodes[p_id][
            "label_type"
        ] in danger_types and get_node_evaluation_results(
            method, graph, p_id, rules
        ):
            return True
    return False


def is_insecure_cookie(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []

    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        n_attrs = graph.nodes[n_id]
        m_name = n_attrs["expression"].split(".")[-1]
        expr_id = n_attrs["expression_id"]
        if (
            m_name == "cookie"
            and graph.nodes[expr_id]["label_type"] == "MemberAccess"
            and graph.nodes[expr_id].get("member") in {"res", "response"}
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and is_insecure_param(method, graph, al_id)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
