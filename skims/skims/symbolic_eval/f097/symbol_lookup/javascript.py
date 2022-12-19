from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def javascript_has_reverse_tabnabbing(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.triggers.add(args.graph.nodes[args.n_id]["symbol"])
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
