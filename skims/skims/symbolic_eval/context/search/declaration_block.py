from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    for c_id in g.adj_cfg(args.graph, args.n_id):
        if args.symbol == args.graph.nodes[c_id]["name"]:
            yield True, c_id
            break
