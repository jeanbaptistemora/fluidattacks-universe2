from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_jpa_like(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"][1:-1]
        if len(args.triggers) == 0:
            args.triggers.add(member_str)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + member_str)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
