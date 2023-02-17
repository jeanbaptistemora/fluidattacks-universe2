from collections.abc import (
    Iterator,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from utils import (
    graph as g,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    for c_id in g.adj_cfg(args.graph, args.n_id):
        if (
            args.graph.nodes[c_id]["label_type"] == "VariableDeclaration"
            and args.graph.nodes[c_id]["variable"] == args.symbol
        ):
            yield True, c_id
            break
