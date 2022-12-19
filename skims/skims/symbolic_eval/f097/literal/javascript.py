from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def javascript_has_reverse_tabnabbing(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"][1:-1]
        args.evaluation[args.n_id] = True
        args.triggers.add(member_str)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
