from collections.abc import (
    Iterator,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from symbolic_eval.context.utils import (
    build_ctx,
)
from utils import (
    graph as g,
)

MODIFYING_METHODS = {"add", "push", "put"}


def method_modifies_symbol(args: SearchArgs) -> bool:
    n_attr = args.graph.nodes[args.n_id]
    expr_split = n_attr["expression"].split(".")
    if expr_split[-1] in MODIFYING_METHODS:
        obj_id = n_attr.get("object_id")
        if (
            obj_id and args.symbol == args.graph.nodes[obj_id].get("symbol")
        ) or (len(expr_split) > 1 and args.symbol in expr_split[0:-1]):
            return True
    return False


def search(args: SearchArgs) -> Iterator[SearchResult]:
    if not args.def_only:
        if method_modifies_symbol(args):
            yield False, args.n_id
        else:
            if "ctx_evaluated" not in args.graph.nodes[args.n_id]:
                build_ctx(args.graph, args.n_id, types={"SymbolLookup"})

            for c_id in g.adj_ctx(args.graph, args.n_id):
                if args.symbol == args.graph.nodes[c_id]["symbol"]:
                    yield False, c_id
