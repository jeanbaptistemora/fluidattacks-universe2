from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def client_storage(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        args.triggers.add(args.graph.nodes[args.n_id]["value"][1:-1])
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
