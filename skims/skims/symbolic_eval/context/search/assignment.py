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
    assign_id = g.adj_ast(args.graph, args.n_id)[0]
    if args.symbol == args.graph.nodes[assign_id].get("symbol"):
        yield True, args.n_id
