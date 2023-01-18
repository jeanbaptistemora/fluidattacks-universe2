from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_compression(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        literal_value := args.graph.nodes[args.n_id].get("value")
    ) and literal_value == '"gzip"':
        args.triggers.add("gzip")
        args.triggers.add(args.n_id)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
