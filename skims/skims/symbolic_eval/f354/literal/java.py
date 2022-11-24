from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_size_limit(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if int(args.graph.nodes[args.n_id]["value"]) > 8388608:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
