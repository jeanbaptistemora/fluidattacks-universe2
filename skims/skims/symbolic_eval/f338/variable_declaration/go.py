from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)


def go_variable_is_harcoded(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    value_id = args.graph.nodes[args.n_id]["value_id"]
    child = adj_ast(args.graph, value_id)
    if child:
        child_attrs = args.graph.nodes[child[0]]

        if (
            child_attrs["label_type"] == "Literal"
            and child_attrs["value_type"] == "string"
        ):
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
