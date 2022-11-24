from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insecure_cors_origin(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"] == '"*"':
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
