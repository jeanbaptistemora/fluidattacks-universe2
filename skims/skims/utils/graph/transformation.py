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


def yield_c_sharp_nested_identifiers(
    graph: graph_model.Graph,
    n_id: str,
    nested_key: str,
    keys: Optional[List[str]] = None,
) -> Iterable[str]:
    match_access = g.match_ast_group(
        graph,
        n_id,
        nested_key,
        "identifier",
        "generic_name",
        "this_expression",
        "invocation_expression",
        ".",
    )

    if (access := match_access[nested_key]) or (
        access := match_access["invocation_expression"]
    ):
        yield from yield_c_sharp_nested_identifiers(
            graph,
            access.pop(),
            nested_key=nested_key,
            keys=keys,
        )

    if id_vals := match_access["identifier"]:
        yield from [graph.nodes[id_val]["label_text"] for id_val in id_vals]

    if this := match_access["this_expression"]:
        yield graph.nodes[this.pop()]["label_text"]

    if generics := match_access["generic_name"]:
        generic_match = g.match_ast(
            graph, generics.pop(), "identifier", "type_argument_list"
        )

        # this two variables always exist but the type is Optional[str]
        identifier_id = str(generic_match["identifier"])
        type_arg_id = str(generic_match["type_argument_list"])

        ident_val = graph.nodes[identifier_id]["label_text"]
        types = g.match_ast_group_d(graph, type_arg_id, "identifier")
        type_list = ",".join([graph.nodes[t]["label_text"] for t in types])

        yield f"{ident_val}<{type_list}>"


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


def build_member_access_expression_key(
    graph: graph_model.Graph,
    n_id: str,
) -> str:
    mem_acces = "member_access_expression"
    return ".".join(yield_c_sharp_nested_identifiers(graph, n_id, mem_acces))


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
