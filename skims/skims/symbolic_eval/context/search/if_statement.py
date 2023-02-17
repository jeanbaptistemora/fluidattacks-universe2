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


def search(args: SearchArgs) -> Iterator[SearchResult]:
    if not args.def_only:
        if "ctx_evaluated" not in args.graph.nodes[args.n_id]:
            build_ctx(
                args.graph,
                args.n_id,
                types={"SymbolLookup", "MethodInvocation"},
            )

        for c_id in g.adj_ctx(args.graph, args.n_id):
            if args.symbol == args.graph.nodes[c_id].get("symbol"):
                yield False, c_id
            if (
                m_expr := args.graph.nodes[c_id].get("expression")
            ) and m_expr.startswith(args.symbol):
                yield False, c_id
