from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insecure_cors_origin(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if "CorsPolicy" in args.graph.nodes[args.n_id]["name"]:
        args.triggers.add("CorsObject")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
