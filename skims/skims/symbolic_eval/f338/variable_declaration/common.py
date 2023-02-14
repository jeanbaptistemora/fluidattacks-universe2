from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def variable_is_harcoded(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    child_id = args.graph.nodes[args.n_id]["value_id"]
    child_attrs = args.graph.nodes[child_id]

    if (
        child_attrs["label_type"] == "Literal"
        and child_attrs["value_type"] == "string"
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
