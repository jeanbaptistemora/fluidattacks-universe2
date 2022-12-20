from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def unsafe_xss_content(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"][1:-1]
        if "<!DOCTYPE html>" in member_str:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
