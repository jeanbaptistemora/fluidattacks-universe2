from model import (
    graph_model,
)
from typing import (
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
        ".",
    )
    if identifiers := match_access["identifier"]:
        keys = [*identifiers, *keys]
    if access := match_access[nested_key]:
        keys = _build_nested_identifier_ids(
            graph,
            access.pop(),
            nested_key=nested_key,
            keys=keys,
        )
    if this := match_access["this_expression"]:
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


def build_member_access_expression_key(
    graph: graph_model.Graph,
    n_id: str,
) -> str:
    keys = build_member_access_expression_isd(graph, n_id)
    identifiers = tuple(graph.nodes[key]["label_text"] for key in keys)
    return ".".join(identifiers)


def build_qualified_name(graph: graph_model.Graph, qualified_id: str) -> str:
    keys = _build_nested_identifier_ids(graph, qualified_id, "qualified_name")
    identifiers = tuple(graph.nodes[key]["label_text"] for key in keys)
    return ".".join(identifiers)


def build_type_name(
    graph: graph_model.Graph,
    identifier_id: str,
) -> Optional[str]:
    node_type = graph.nodes[identifier_id]["label_type"]
    if node_type == "identifier":
        return graph.nodes[identifier_id]["label_text"]
    if node_type == "qualified_name":
        return build_qualified_name(graph, identifier_id)
    return None
