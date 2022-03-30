from model.graph_model import (
    Graph,
    GraphShard,
    NId,
)
from symbolic_eval.utils import (
    filter_ast,
)
from typing import (
    Iterator,
    Set,
)
from utils.graph import (
    get_ast_childs,
    lookup_first_cfg_parent,
    pred_cfg,
)


def get_method_param_by_obj(
    shard: GraphShard, n_id: str, object_type: str
) -> str:
    for _class in (
        shard.metadata.c_sharp.classes.values()
        if shard.metadata.c_sharp
        else []
    ):
        if "." + get_method_name(shard.graph, n_id) in _class.methods.keys():
            parameters = _class.methods[
                "." + get_method_name(shard.graph, n_id)
            ].parameters
            param_keys = parameters.keys() if parameters else []
            for param in param_keys:
                params = _class.methods[
                    "." + get_method_name(shard.graph, n_id)
                ].parameters
                if params and params[param].type_name == object_type:
                    return param
    return ""


def get_method_name(graph: Graph, n_id: str) -> str:
    node_cfg = lookup_first_cfg_parent(graph, n_id)
    while graph.nodes[node_cfg].get("label_type") != "method_declaration":
        node_cfg = pred_cfg(graph, node_cfg, depth=1)[0]
    method_name = get_ast_childs(graph, node_cfg, "identifier")[0]
    return graph.nodes[method_name].get("label_text")


def search_method_invocation_naive(
    graph: Graph, methods: Set[str]
) -> Iterator[NId]:
    for n_id in filter_ast(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id
