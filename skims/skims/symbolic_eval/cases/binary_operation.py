from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    op_attr = args.graph.nodes[args.n_id]
    d_l_expr = args.generic(args.fork_n_id(op_attr["left_id"]))
    d_r_expr = args.generic(args.fork_n_id(op_attr["right_id"]))

    args.graph.nodes[args.n_id]["danger"] = d_l_expr or d_r_expr

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return args.graph.nodes[args.n_id]["danger"]
