from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def is_request_form(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    return ma_attr["expression"] == "Request" and ma_attr["member"] == "Form"


def is_select_single_node(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    expr_id = ma_attr["expression_id"]

    if args.evaluation[expr_id] and ma_attr["member"] == "SelectSingleNode":
        return True
    return False


def evaluate(args: SymbolicEvalArgs) -> bool:
    if is_request_form(args) or is_select_single_node(args):
        args.evaluation[args.n_id] = True

    return args.evaluation[args.n_id]
