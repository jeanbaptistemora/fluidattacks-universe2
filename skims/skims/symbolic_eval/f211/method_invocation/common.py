from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)

SAFE_METHODS = {"'escape-string-regexp'"}


def common_regex_injection(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["expression"] == "require":
        arg_list = ma_attr["arguments_id"]
        arg_node = g.adj_ast(args.graph, arg_list)[0]
        if args.graph.nodes[arg_node]["value"] in SAFE_METHODS:
            args.triggers.add("SafeValidation")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
