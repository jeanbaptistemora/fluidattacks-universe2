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
        if args.graph.nodes[c_id]["label_type"] == "FieldDeclaration":
            var_id = g.match_ast_d(args.graph, c_id, "VariableDeclaration")
            if var_id and args.graph.nodes[var_id]["variable"] == args.symbol:
                yield True, c_id
                break
