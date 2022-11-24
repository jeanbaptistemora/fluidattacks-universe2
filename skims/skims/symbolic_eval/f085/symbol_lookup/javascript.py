from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def client_storage(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.triggers.add(args.graph.nodes[args.n_id]["symbol"])
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
