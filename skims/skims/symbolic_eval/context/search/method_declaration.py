from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from symbolic_eval.context.utils import (
    build_ctx,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    if args.graph.nodes[args.n_id]["name"] == args.symbol:
        yield True, args.n_id
    else:
        if "ctx_evaluated" not in args.graph.nodes[args.n_id]:
            build_ctx(args.graph, args.n_id, types={"Parameter"})

        for c_id in g.adj_ctx(args.graph, args.n_id):
            if args.symbol == args.graph.nodes[c_id]["variable"]:
                yield True, c_id
                break
