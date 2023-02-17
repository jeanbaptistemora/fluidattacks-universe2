from collections.abc import (
    Iterator,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    var_id = args.graph.nodes[args.n_id]["declaration_id"]

    if args.symbol == args.graph.nodes[var_id].get("variable"):
        yield True, args.n_id
