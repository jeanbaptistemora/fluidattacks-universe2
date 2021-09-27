from model.graph_model import (
    Graph,
)
from typing import (
    Iterable,
    List,
    Tuple,
)
from utils.graph import (
    adj_ast,
)


def get_node_text(graph: Graph, n_id: str) -> str:
    return graph.nodes[n_id].get("label_text", "")


def iter_childs(graph: Graph, n_id: str) -> Iterable[str]:
    for c_id in adj_ast(graph, n_id):
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
