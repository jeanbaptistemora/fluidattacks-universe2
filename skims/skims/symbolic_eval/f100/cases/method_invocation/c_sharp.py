from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    mi_attrs = args.graph.nodes[args.n_id]

    al_id = mi_attrs["arguments_id"]
    expr_id = mi_attrs["expression_id"]
    ma_attrs = args.graph.nodes[expr_id]

    if (
        args.graph.nodes[expr_id]["label_type"] == "MemberAccess"
        and ma_attrs["expression"] == "WebRequest"
        and ma_attrs["member"] == "Create"
        and args.evaluation[al_id]
    ):
        args.evaluation[args.n_id] = True
    else:
        args.evaluation[args.n_id] = False

    return args.evaluation[args.n_id]
