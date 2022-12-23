from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Iterable,
    Optional,
    Tuple,
)
from utils.graph import (
    match_ast,
    matching_nodes,
)


def concatenate_name(
    graph: Graph, n_id: NId, name: Optional[str] = None
) -> str:
    if name:
        prev_str = "." + name
    else:
        prev_str = ""

    node_type = graph.nodes[n_id]["label_type"]
    if node_type == "MethodInvocation":
        expr = graph.nodes[n_id]["expression"]
        if graph.nodes[n_id].get("object_id") and (
            next_node := match_ast(graph, n_id)["__0__"]
        ):
            expr = concatenate_name(graph, next_node, expr)
    elif node_type == "SymbolLookup":
        expr = graph.nodes[n_id]["symbol"]
    elif node_type == "FieldAccess":
        expr = graph.nodes[n_id]["field_text"]
    else:
        expr = ""
    return expr + prev_str


def yield_method_invocation_syntax_graph(
    graph: Graph,
) -> Iterable[Tuple[str, str]]:
    for n_id in matching_nodes(graph, label_type="MethodInvocation"):
        method_name = concatenate_name(graph, n_id)
        yield n_id, method_name
