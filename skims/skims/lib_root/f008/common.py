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
from typing import (
    List,
    Set,
)
from utils import (
    graph as g,
)


def is_node_vuln(
    graph: Graph, n_id: NId, danger_set: Set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def unsafe_xss_content_nodes(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_set = {"userconnection"}

    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
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
                and is_node_vuln(graph, args_ids[0], danger_set, method)
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
