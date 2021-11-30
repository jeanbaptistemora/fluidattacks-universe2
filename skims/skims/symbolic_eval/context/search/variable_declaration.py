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
    if args.graph.nodes[args.n_id]["variable"] == args.symbol:
        yield True, args.n_id
    elif not args.def_only:
        if "ctx_evaluated" not in args.graph.nodes[args.n_id]:
            build_ctx(args.graph, args.n_id, types={"SymbolLookup"})

        for c_id in g.adj_ctx(args.graph, args.n_id):
            if args.symbol == args.graph.nodes[c_id]["symbol"]:
                yield False, c_id
