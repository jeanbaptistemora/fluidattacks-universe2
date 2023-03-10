from collections.abc import (
    Iterator,
)
from model.graph_model import (
    Graph,
    NId,
)
from utils.graph import (
    match_ast,
    matching_nodes,
)


def concatenate_name(graph: Graph, n_id: NId, name: str | None = None) -> str:
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
    else:
        expr = ""
    return expr + prev_str


def yield_method_invocation_syntax_graph(
    graph: Graph,
) -> Iterator[tuple[str, str]]:
    for n_id in matching_nodes(graph, label_type="MethodInvocation"):
        method_name = concatenate_name(graph, n_id)
        yield n_id, method_name
