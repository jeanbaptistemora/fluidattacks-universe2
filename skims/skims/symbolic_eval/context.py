from model.graph_model import (
    Graph,
)
from symbolic_eval.types import (
    Path,
)
from symbolic_eval.utils import (
    filter_ast,
)
from typing import (
    Iterator,
    Tuple,
)
from utils import (
    graph as g,
)


def build_context(graph: Graph, n_id: str) -> None:
    types = {"SymbolLookup", "Parameter"}
    for c_id in filter_ast(graph, n_id, types, strict=True):
        graph.add_edge(n_id, c_id, label_ctx="CTX")
    graph.nodes[n_id]["ctx_evaluated"] = True


def node_search(graph: Graph, cfg_id: str, symbol_id: str) -> Iterator[str]:
    if "ctx_evaluated" not in graph.nodes[cfg_id]:
        build_context(graph, cfg_id)

    symbol = graph.nodes[symbol_id]["symbol"]
    node_attr = graph.nodes[cfg_id]

    # Search childs
    for c_id in g.adj_ctx(graph, cfg_id):
        if graph.nodes[c_id]["symbol"] == symbol:
            yield c_id

    # Search current node
    if node_attr.get("variable") == symbol:
        yield cfg_id


def back_search(
    graph: Graph, path: Path, symbol_id: str
) -> Iterator[Tuple[str, str]]:
    keep_iter = True
    cfg_nodes = iter(path)

    while keep_iter and (cfg_id := next(cfg_nodes, None)):
        for n_id in node_search(graph, cfg_id, symbol_id):
            yield cfg_id, n_id

            # if n_id is the lookup resolution stop search
            # otherwise is a symbol usage, continue searching
            if graph.nodes[n_id]["label_type"] != "SymbolLookup":
                keep_iter = False


def search(
    graph: Graph, path: Path, symbol_id: str
) -> Iterator[Tuple[str, str]]:
    return reversed(list(back_search(graph, path, symbol_id)))
