from model.graph_model import (
    Graph,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Iterator,
    Set,
)
from utils import (
    graph as g,
)


def iter_ast(graph: Graph, n_id: str, strict: bool = False) -> Iterator[str]:
    if not strict or not g.is_connected_to_cfg(graph, n_id):
        yield n_id

    for c_id in g.adj_ast(graph, n_id):
        if strict and g.is_connected_to_cfg(graph, c_id):
            continue
        yield from iter_ast(graph, c_id)


def iter_paths(graph: Graph, cfg_n_id: str) -> Iterator[Path]:
    path = [cfg_n_id]
    parents = g.pred_cfg(graph, cfg_n_id)

    if not parents:
        yield path

    for parent in parents:
        for sub_path in get_paths(graph, parent):
            yield path + sub_path


def get_paths(graph: Graph, n_id: str) -> Iterator[Path]:
    yield from iter_paths(graph, g.lookup_first_cfg_parent(graph, n_id))


def filter_ast(
    graph: Graph, n_id: str, types: Set[str], strict: bool = False
) -> Iterator[str]:
    for c_id in iter_ast(graph, n_id, strict):
        if graph.nodes[c_id]["label_type"] in types:
            yield c_id


def search_method_invocation(graph: Graph, methods: Set[str]) -> Iterator[str]:
    for n_id in filter_ast(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id


def get_lookup_path(graph: Graph, path: Path, symbol_id: str) -> Path:
    cfg_parent = g.lookup_first_cfg_parent(graph, symbol_id)
    cfg_parent_idx = path.index(cfg_parent)  # current instruction idx
    return path[cfg_parent_idx + 1 :]  # from previus instruction idx
