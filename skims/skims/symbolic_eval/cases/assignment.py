from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    op_attr = args.graph.nodes[args.n_id]
    d_l_expr = args.generic(args.fork_n_id(op_attr["variable_id"])).danger
    d_r_expr = args.generic(args.fork_n_id(op_attr["value_id"])).danger

    args.evaluation[args.n_id] = d_l_expr or d_r_expr

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
