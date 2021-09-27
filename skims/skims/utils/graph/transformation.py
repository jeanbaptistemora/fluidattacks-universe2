from model.graph_model import (
    Graph,
)
from typing import (
    cast,
    Iterable,
    List,
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)


def get_identifiers_ids(
    graph: Graph,
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
    graph: Graph,
    n_id: str,
    nested_key: str,
) -> Optional[str]:
    return next(iter(get_identifiers_ids(graph, n_id, nested_key)), None)


def get_identifiers_ids_js(
    graph: Graph,
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


def get_node_text(graph: Graph, n_id: str) -> str:
    return graph.nodes[n_id].get("label_text", "")


def iter_childs(graph: Graph, n_id: str) -> Iterable[str]:
    for c_id in g.adj_ast(graph, n_id):
        yield from iter_childs(graph, c_id)
    yield n_id


def lazy_text_childs(graph: Graph, n_id: str) -> Iterable[str]:
    for c_id in iter_childs(graph, n_id):
        if "label_text" in graph.nodes[c_id]:
            yield c_id


def lazy_childs_text(graph: Graph, n_id: str) -> Iterable[str]:
    for c_id in lazy_text_childs(graph, n_id):
        yield graph.nodes[c_id]["label_text"]


def lazy_childs_text_ids(graph: Graph, n_id: str) -> Iterable[Tuple[str, str]]:
    for c_id in lazy_text_childs(graph, n_id):
        yield get_node_text(graph, c_id), c_id


def lazy_n_ids_to_str(graph: Graph, n_ids: Iterable[str]) -> Iterable[str]:
    for n_id in n_ids:
        yield get_node_text(graph, n_id)


def get_childs(graph: Graph, n_id: str) -> List[str]:
    return list(iter_childs(graph, n_id))


def get_text_childs(graph: Graph, n_id: str) -> List[str]:
    return list(lazy_text_childs(graph, n_id))


def get_childs_text(graph: Graph, n_id: str) -> List[str]:
    return list(lazy_childs_text(graph, n_id))


def get_childs_text_with_ids(graph: Graph, n_id: str) -> List[Tuple[str, str]]:
    return list(lazy_childs_text_ids(graph, n_id))


def n_ids_to_str(graph: Graph, n_ids: Iterable[str], sep: str = "") -> str:
    return sep.join(lazy_n_ids_to_str(graph, n_ids))


def node_to_str(graph: Graph, n_id: str, sep: str = "") -> str:
    return sep.join(lazy_childs_text(graph, n_id))
