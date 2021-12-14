from model.graph_model import (
    Graph,
    NId,
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


def iter_ast(graph: Graph, n_id: NId, strict: bool = False) -> Iterator[NId]:
    if not strict or not g.is_connected_to_cfg(graph, n_id):
        yield n_id

    for c_id in g.adj_ast(graph, n_id):
        if strict and g.is_connected_to_cfg(graph, c_id):
            continue
        yield from iter_ast(graph, c_id)


def iter_backward_paths(graph: Graph, cfg_n_id: NId) -> Iterator[Path]:
    path = [cfg_n_id]
    parents = g.pred_cfg(graph, cfg_n_id)

    if not parents:
        yield path

    for parent in parents:
        for sub_path in iter_backward_paths(graph, parent):
            yield path + sub_path


def get_backward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    cfg_id = g.lookup_first_cfg_parent(graph, n_id)
    yield from iter_backward_paths(graph, cfg_id)


def iter_forward_paths(graph: Graph, cfg_id: NId) -> Iterator[Path]:
    path = [cfg_id]
    childs = g.adj_cfg(graph, cfg_id)

    if not childs:
        yield path

    for child in childs:
        for sub_path in iter_forward_paths(graph, child):
            yield path + sub_path


def get_forward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    cfg_id = g.lookup_first_cfg_parent(graph, n_id)
    yield from iter_forward_paths(graph, cfg_id)


def invert_path(path: Path) -> Path:
    inv_path = path.copy()
    inv_path.reverse()
    return inv_path


def get_inv_forward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    for path in get_forward_paths(graph, n_id):
        yield invert_path(path)


def filter_ast(
    graph: Graph, n_id: NId, types: Set[str], strict: bool = False
) -> Iterator[NId]:
    for c_id in iter_ast(graph, n_id, strict):
        if graph.nodes[c_id]["label_type"] in types:
            yield c_id


def search_method_invocation(graph: Graph, methods: Set[str]) -> Iterator[NId]:
    for n_id in filter_ast(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id


def get_lookup_path(graph: Graph, path: Path, symbol_id: NId) -> Path:
    cfg_parent = g.lookup_first_cfg_parent(graph, symbol_id)
    cfg_parent_idx = path.index(cfg_parent)  # current instruction idx
    return path[cfg_parent_idx + 1 :]  # from previus instruction idx
