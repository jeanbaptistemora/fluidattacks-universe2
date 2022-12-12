from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def java_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = False

    if ma_attr["expression"] == "quote":
        child = g.get_ast_childs(args.graph, args.n_id, "SymbolLookup")

        if args.graph.nodes[child[0]]["symbol"] == "Pattern":
            args.triggers.add("SafeRegex")
    else:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
