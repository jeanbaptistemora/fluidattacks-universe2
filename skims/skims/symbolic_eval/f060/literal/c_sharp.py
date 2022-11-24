from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insecure_certificate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"] == "true":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
