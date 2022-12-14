from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def javascript_insecure_cookie(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    childs = g.get_ast_childs(args.graph, args.n_id, "SymbolLookup", depth=2)
    for child in childs:
        if args.graph.nodes[child]["symbol"] == "token":
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
