from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_node_vuln(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
) -> bool:
    rules = {"InsecureCookie"}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def is_insecure_param(
    graph: Graph, params_ids: tuple, method: MethodsEnum
) -> bool:
    for p_id in params_ids:
        n_attrs = graph.nodes[p_id]
        label_type = n_attrs["label_type"]
        if label_type in {"Object", "SymbolLookup"} and is_node_vuln(
            graph, p_id, method
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
            and graph.nodes[expr_id]["member"] in {"res", "response"}
        ):
            al_id = graph.nodes[n_id].get("arguments_id")
            if (
                al_id
                and (args_ids := g.adj_ast(graph, al_id))
                and is_insecure_param(graph, args_ids, method)
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
