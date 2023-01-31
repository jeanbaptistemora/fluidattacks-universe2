from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_jwt_token(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    value = args.graph.nodes[args.n_id]["value"][1:-1].lower()
    if value == "none":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
