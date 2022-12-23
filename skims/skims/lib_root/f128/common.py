from lib_root.utilities.javascript import (
    file_imports_module,
)
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
    if file_imports_module(graph, "ngx-cookie-service"):
        for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
            expression = graph.nodes[n_id].get("expression")
            if any(exp in expression for exp in danger_methods) and has_args(
                graph, n_id
            ):
                vuln_nodes.append(n_id)

    return vuln_nodes
