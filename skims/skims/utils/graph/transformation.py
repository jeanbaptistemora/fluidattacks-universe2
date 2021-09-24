from model import (
    graph_model,
)
from typing import (
    cast,
    Iterable,
    List,
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


def build_js_member_expression_ids(
    graph: graph_model.Graph, qualified_id: str
) -> List[str]:
    return _build_nested_identifier_ids_js(
        graph,
        qualified_id,
        "member_expression",
    )
