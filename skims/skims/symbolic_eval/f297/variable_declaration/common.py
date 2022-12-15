from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def common_sql_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    child_id = args.graph.nodes[args.n_id]["value_id"]
    child_attrs = args.graph.nodes[child_id]

    if (
        child_attrs["label_type"] == "BinaryOperation"
        and child_attrs["operator"] == "+"
    ):
        args.triggers.add("NonParametrizedQuery")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
