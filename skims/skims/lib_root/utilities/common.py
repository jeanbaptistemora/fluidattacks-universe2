from model.graph_model import (
    Graph,
)
from utils.graph import (
    get_ast_childs,
    lookup_first_cfg_parent,
    pred_cfg,
)


def get_method_name(graph: Graph, n_id: str) -> str:
    node_cfg = lookup_first_cfg_parent(graph, n_id)
    while graph.nodes[node_cfg].get("label_type") != "method_declaration":
        node_cfg = pred_cfg(graph, node_cfg, depth=1)[0]
    method_name = get_ast_childs(graph, node_cfg, "identifier")[0]
    return graph.nodes[method_name].get("label_text")
