from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def validation_always_return_true(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    if (
        (return_val_n_id := nodes[args.n_id].get("value_id"))
        and (nodes[return_val_n_id].get("value_type") == "bool")
        and (nodes[return_val_n_id].get("value") == "true")
    ):
        args.triggers.add("return_true")
    else:
        args.triggers.add("return_other")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
