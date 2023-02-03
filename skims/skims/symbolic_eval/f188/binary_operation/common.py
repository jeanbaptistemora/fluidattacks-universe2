from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def has_origin_check(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    left_id = args.graph.nodes[args.n_id]["left_id"]
    if (
        expression := args.graph.nodes[left_id].get("expression")
    ) and expression == "origin":
        right_id = args.graph.nodes[args.n_id]["right_id"]
        if (
            member_access := args.graph.nodes[right_id].get("member")
        ) and member_access == "window.location":
            args.triggers.add("WindowOriginChecked")
        if (
            value_type := args.graph.nodes[right_id].get("value_type")
        ) and value_type == "string":
            args.triggers.add("TypeOriginChecked")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
