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


def import_cookie_service(graph: Graph) -> bool:
    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="Import"),
    ):
        expression = graph.nodes[n_id].get("expression")
        if expression == "'ngx-cookie-service'":
            return True
    return False


def has_args(graph: Graph, method_id: NId) -> bool:

    args_id = g.get_ast_childs(graph, method_id, "ArgumentList")
    if args_id:
        args_nids = g.adj_ast(graph, args_id[0])
        if args_nids and len(args_nids) >= 1:
            return True
    return False


def insecure_cookies(graph: Graph) -> List[str]:
    vuln_nodes: List[str] = []
    danger_methods = {
        "cookieService.set",
        "CookieService.set",
    }
    if import_cookie_service(graph=graph):
        for n_id in g.filter_nodes(
            graph,
            nodes=graph.nodes,
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            expression = graph.nodes[n_id].get("expression")
            if any(exp in expression for exp in danger_methods) and has_args(
                graph, n_id
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
