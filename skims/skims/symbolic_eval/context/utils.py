from collections.abc import (
    Set,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.utils import (
    filter_ast,
)


def build_ctx(graph: Graph, n_id: NId, types: Set[str]) -> None:
    for c_id in filter_ast(graph, n_id, types, strict=True):
        graph.add_edge(n_id, c_id, label_ctx="CTX")
    graph.nodes[n_id]["ctx_evaluated"] = True
