from symbolic_eval.common import (
    check_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def is_select_single_node(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    expr_id = ma_attr["expression_id"]

    if args.evaluation[expr_id] and ma_attr["member"] == "SelectSingleNode":
        return True
    return False


def cs_xpath_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_http_inputs(args) or is_select_single_node(args):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
