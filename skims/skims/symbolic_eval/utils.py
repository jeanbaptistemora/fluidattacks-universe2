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


def iter_nodes(graph: Graph, n_id: str) -> Iterator[str]:
    yield n_id
    for c_id in g.adj_ast(graph, n_id):
        yield from iter_nodes(graph, c_id)


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


def filter_nodes(graph: Graph, n_id: str, types: Set[str]) -> Iterator[str]:
    for c_id in iter_nodes(graph, n_id):
        if graph.nodes[c_id]["label_type"] in types:
            yield c_id


def search_method_invocation(graph: Graph, methods: Set[str]) -> Iterator[str]:
    for n_id in filter_nodes(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id
