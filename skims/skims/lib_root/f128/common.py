from lib_root.utilities.javascript import (
    file_imports_module,
)
from model.graph_model import (
    Graph,
)
from utils import (
    graph as g,
)


def insecure_cookies(graph: Graph) -> list[str]:
    vuln_nodes: list[str] = []
    if not file_imports_module(graph, "ngx-cookie-service"):
        return vuln_nodes
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        if (
            (expr := graph.nodes[n_id].get("expression"))
            and expr.lower().endswith("cookieservice.set")
            and (args_id := g.match_ast_d(graph, n_id, "ArgumentList"))
            and (args_nids := g.adj_ast(graph, args_id[0]))
            and len(args_nids) > 1
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
