from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f004.member_access import (
    evaluate as evaluate_member_access_f004,
)
from symbolic_eval.f021.member_access import (
    evaluate as evaluate_member_access_f021,
)
from symbolic_eval.f100.member_access import (
    evaluate as evaluate_member_access_f100,
)
from symbolic_eval.f239.member_access import (
    evaluate as evaluate_member_access_f239,
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
    FindingEnum.F004: evaluate_member_access_f004,
    FindingEnum.F021: evaluate_member_access_f021,
    FindingEnum.F100: evaluate_member_access_f100,
    FindingEnum.F239: evaluate_member_access_f239,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    args.evaluation[args.n_id] = args.generic(args.fork_n_id(expr_id)).danger
    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
