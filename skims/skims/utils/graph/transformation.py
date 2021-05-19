# Standar library
from typing import (
    List,
    Optional,
)
from model import graph_model

# Local imports
from utils import graph as g


def build_member_access_expression_isd(
    graph: graph_model.Graph,
    n_id: str,
    keys: Optional[List[str]] = None,
) -> List[str]:
    keys = keys or list()
    match_access = g.match_ast_group(
        graph,
        n_id,
        "identifier",
        "member_access_expression",
        "this_expression",
        ".",
    )
    if identifiers := match_access["identifier"]:
        keys = [*identifiers, *keys]
    if access := match_access["member_access_expression"]:
        keys = build_member_access_expression_isd(graph, access.pop(), keys)
    if this := match_access["this_expression"]:
        keys.append(this.pop())

    return keys


def build_member_access_expression_key(
    graph: graph_model.Graph,
    n_id: str,
    keys: Optional[List[str]] = None,
) -> str:
    keys = build_member_access_expression_isd(graph, n_id, keys)
    identifiers = tuple(graph.nodes[key]["label_text"] for key in keys)
    return ".".join(identifiers)
