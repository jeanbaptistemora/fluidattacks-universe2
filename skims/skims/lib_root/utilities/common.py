from model.graph_model import (
    Graph,
    GraphShard,
)
from utils.graph import (
    get_ast_childs,
    lookup_first_cfg_parent,
    pred_cfg,
)


def get_method_param_by_obj(
    shard: GraphShard, n_id: str, object_type: str
) -> str:
    for _class in shard.metadata.c_sharp.classes.values():
        if "." + get_method_name(shard.graph, n_id) in _class.methods.keys():
            param_keys = _class.methods[
                "." + get_method_name(shard.graph, n_id)
            ].parameters.keys()
            for param in param_keys:
                if (
                    _class.methods["." + get_method_name(shard.graph, n_id)]
                    .parameters[param]
                    .type_name
                    == object_type
                ):
                    return param
    return ""


def get_method_name(graph: Graph, n_id: str) -> str:
    node_cfg = lookup_first_cfg_parent(graph, n_id)
    while graph.nodes[node_cfg].get("label_type") != "method_declaration":
        node_cfg = pred_cfg(graph, node_cfg, depth=1)[0]
    method_name = get_ast_childs(graph, node_cfg, "identifier")[0]
    return graph.nodes[method_name].get("label_text")
