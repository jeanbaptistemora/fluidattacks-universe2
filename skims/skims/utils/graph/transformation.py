from model import (
    graph_model,
)
from typing import (
    cast,
    List,
    Optional,
)
from utils import (
    graph as g,
)


def _build_nested_identifier_ids(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
    keys: Optional[List[str]] = None,
) -> List[str]:
    keys = keys or list()
    match_access = g.match_ast_group(
        graph,
        n_id,
        "identifier",
        nested_key,
        "this_expression",
        "invocation_expression",
        ".",
    )
    if identifiers := match_access["identifier"]:
        keys = [*identifiers, *keys]
    if (access := match_access[nested_key]) or (
        access := match_access["invocation_expression"]
    ):
        keys = _build_nested_identifier_ids(
            graph,
            access.pop(),
            nested_key=nested_key,
            keys=keys,
        )
    if this := match_access["this_expression"]:
        keys.append(this.pop())

    return keys


def node_to_str(graph: graph_model.Graph, n_id: str) -> str:
    node = graph.nodes[n_id]
    result_str = node["label_text"] if "label_text" in node else ""
    for c_id in g.adj_ast(graph, n_id):
        result_str += node_to_str(graph, c_id)
    return result_str


def _build_nested_identifier_ids_js(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
    keys: Optional[List[str]] = None,
) -> List[str]:
    keys = keys or list()
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
    if identifiers := match_access["property_identifier"]:
        keys = [*identifiers, *keys]
    if (access := match_access[nested_key]) or (
        access := match_access["call_expression"]
    ):
        keys = _build_nested_identifier_ids_js(
            graph,
            access.pop(),
            nested_key=nested_key,
            keys=keys,
        )

    if identifiers := match_access["identifier"]:
        keys = [*identifiers, *keys]
    if element := match_access.get("__0__"):
        keys = [*keys, cast(str, element)]
    if this := match_access["this"]:
        keys.append(this.pop())

    return keys


def build_member_access_expression_isd(
    graph: graph_model.Graph,
    n_id: str,
) -> List[str]:
    return _build_nested_identifier_ids(
        graph,
        n_id,
        "member_access_expression",
    )


def build_qualified_name(graph: graph_model.Graph, qualified_id: str) -> str:
    keys = _build_nested_identifier_ids(graph, qualified_id, "qualified_name")
    identifiers = tuple(graph.nodes[key]["label_text"] for key in keys)
    return ".".join(identifiers)


def build_js_member_expression_key(
    graph: graph_model.Graph, qualified_id: str
) -> str:
    keys = build_js_member_expression_ids(graph, qualified_id)
    identifiers = tuple(
        graph.nodes[key]["label_text"]
        for key in keys
        if "label_text" in graph.nodes[key]
    )
    return ".".join(identifiers)


def build_js_member_expression_ids(
    graph: graph_model.Graph, qualified_id: str
) -> List[str]:
    return _build_nested_identifier_ids_js(
        graph,
        qualified_id,
        "member_expression",
    )


def build_type_name(
    graph: graph_model.Graph,
    identifier_id: str,
) -> Optional[str]:
    node_type = graph.nodes[identifier_id]["label_type"]
    if node_type == "identifier":
        return graph.nodes[identifier_id]["label_text"]
    if node_type == "qualified_name":
        return build_qualified_name(graph, identifier_id)
    return graph.nodes[identifier_id].get("label_text")
