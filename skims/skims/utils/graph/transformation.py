from model import (
    graph_model,
)
from typing import (
    cast,
    Iterable,
    Optional,
)
from utils import (
    graph as g,
)


def get_identifiers_ids(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
) -> Iterable[str]:
    match_access = g.match_ast_group(
        graph,
        n_id,
        nested_key,
        "identifier",
        "this_expression",
        "invocation_expression",
        ".",
    )

    if (access := match_access[nested_key]) or (
        access := match_access["invocation_expression"]
    ):
        yield from get_identifiers_ids(graph, access.pop(), nested_key)

    if identifiers := match_access["identifier"]:
        yield from identifiers

    if this := match_access["this_expression"]:
        yield this.pop()


def get_base_identifier_id(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
) -> Optional[str]:
    return next(iter(get_identifiers_ids(graph, n_id, nested_key)), None)


def node_to_str(graph: graph_model.Graph, n_id: str) -> str:
    node = graph.nodes[n_id]
    result_str = node["label_text"] if "label_text" in node else ""
    for c_id in g.adj_ast(graph, n_id):
        result_str += node_to_str(graph, c_id)
    return result_str


def get_identifiers_ids_js(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
) -> Iterable[str]:
    match_access = g.match_ast_group(
        graph,
        n_id,
        "identifier",
        nested_key,
        "this",
        "property_identifier",
        "call_expression",
        ".",
        "arguments",
    )

    if (access := match_access[nested_key]) or (
        access := match_access["call_expression"]
    ):
        yield from get_identifiers_ids_js(graph, access.pop(), nested_key)

    if identifiers := match_access["property_identifier"]:
        yield from identifiers

    if identifiers := match_access["identifier"]:
        yield from identifiers

    if element := match_access.get("__0__"):
        yield cast(str, element)

    if this := match_access["this"]:
        yield this.pop()
