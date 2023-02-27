from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_unverified(graph: Graph, method_id: NId) -> bool:
    al_id = graph.nodes[method_id]["arguments_id"]
    token_varid = g.adj_ast(graph, al_id)[0]
    token_name = graph.nodes[token_varid].get("symbol")

    if not token_name:
        return False

    is_jwt_verified = any(
        graph.nodes[n_path]["label_type"] == "MethodInvocation"
        and graph.nodes[n_path].get("expression") == "jwt.verify"
        and (arl_id := graph.nodes[n_path]["arguments_id"])
        and graph.nodes[g.adj_ast(graph, arl_id)[0]].get("symbol")
        == token_name
        for path in get_backward_paths(graph, method_id)
        for n_path in path
    )
    if is_jwt_verified:
        return False

    # If the token is used as an argument in a methodInvocation previous to
    # the decoding, the vulnerability is not deterministic since this
    # function could be from another file that performs the validation
    for n_id in g.matching_nodes(graph, label_type="SymbolLookup"):
        parent_id = g.pred_ast(graph, n_id, depth=2)[1]
        if (
            n_id != token_varid
            and graph.nodes[n_id]["symbol"] == token_name
            and graph.nodes[parent_id]["label_type"] == "MethodInvocation"
            and (parent_cfg := g.lookup_first_cfg_parent(graph, n_id))
            and any(
                parent_cfg in path and parent_id not in path
                for path in get_backward_paths(graph, method_id)
            )
        ):
            return False

    # Only if neither condition is met, the vuln is deterministic
    return True


def insecure_jwt_decode(graph: Graph) -> list[str]:
    vuln_nodes: list[str] = []
    for n_id in yield_syntax_graph_member_access(graph, {"decode"}):
        parent_id = g.pred_ast(graph, n_id)[0]
        if (
            graph.nodes[n_id].get("member") == "jwt"
            and graph.nodes[parent_id]["label_type"] == "MethodInvocation"
            and (al_id := graph.nodes[parent_id].get("arguments_id"))
            and len(g.adj_ast(graph, al_id)) > 0
            and is_unverified(graph, parent_id)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
