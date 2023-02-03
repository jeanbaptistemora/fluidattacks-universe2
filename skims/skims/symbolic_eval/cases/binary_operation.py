from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f188.binary_operation import (
    evaluate as evaluate_binary_operation_f188,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F188: evaluate_binary_operation_f188,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    op_attr = args.graph.nodes[args.n_id]
    d_l_expr = args.generic(args.fork_n_id(op_attr["left_id"])).danger
    d_r_expr = args.generic(args.fork_n_id(op_attr["right_id"])).danger

    args.evaluation[args.n_id] = d_l_expr or d_r_expr

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
