from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_path_traversal(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "resolve":
        args.triggers.add("resolve")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
