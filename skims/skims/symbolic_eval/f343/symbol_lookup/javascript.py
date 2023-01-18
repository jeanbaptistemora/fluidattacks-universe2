from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_compression(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        symbol := args.graph.nodes[args.n_id].get("symbol")
    ) and symbol == "algorithm":
        args.triggers.add("algorithm")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
