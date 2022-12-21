from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_weak_random(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] in {
        "java.util.Random",
        "java.lang.Math.random",
    }:
        args.triggers.add("weakrandom")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
