from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from model.graph_model import (
    Graph,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def insecure_jwt_decode(graph: Graph) -> list[str]:
    vuln_nodes: list[str] = []
    for n_id in yield_syntax_graph_member_access(graph, {"decode"}):
        if graph.nodes[n_id].get("member") == "jwt" and not any(
            graph.nodes[n_path]["label_type"] == "MethodInvocation"
            and graph.nodes[n_path].get("expression") == "jwt.verify"
            for path in get_backward_paths(graph, n_id)
            for n_path in path
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
