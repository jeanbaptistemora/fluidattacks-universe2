from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def weak_random(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if "Math.random()" in args.graph.nodes[args.n_id]["expression"]:
        args.triggers.add("Random")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
