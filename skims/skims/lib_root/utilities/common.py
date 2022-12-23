from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.utils import (
    filter_ast,
)
from typing import (
    Iterator,
    Set,
)


def search_method_invocation_naive(
    graph: Graph, methods: Set[str]
) -> Iterator[NId]:
    for n_id in filter_ast(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id
