from model.core_model import (
    FindingEnum,
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
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F021: evaluate_member_access_f021,
    FindingEnum.F100: evaluate_member_access_f100,
    FindingEnum.F239: evaluate_member_access_f239,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    args.evaluation[args.n_id] = args.generic(args.fork_n_id(expr_id))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
