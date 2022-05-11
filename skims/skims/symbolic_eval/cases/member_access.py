from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f004.member_access import (
    evaluate as evaluate_member_access_f004,
)
from symbolic_eval.f008.member_access import (
    evaluate as evaluate_member_access_f008,
)
from symbolic_eval.f021.member_access import (
    evaluate as evaluate_member_access_f021,
)
from symbolic_eval.f063.member_access import (
    evaluate as evaluate_member_access_f063,
)
from symbolic_eval.f096.member_access import (
    evaluate as evaluate_member_access_f096,
)
from symbolic_eval.f098.member_access import (
    evaluate as evaluate_member_access_f098,
)
from symbolic_eval.f100.member_access import (
    evaluate as evaluate_member_access_f100,
)
from symbolic_eval.f239.member_access import (
    evaluate as evaluate_member_access_f239,
)
from symbolic_eval.f413.member_access import (
    evaluate as evaluate_member_access_f413,
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
    FindingEnum.F008: evaluate_member_access_f008,
    FindingEnum.F021: evaluate_member_access_f021,
    FindingEnum.F096: evaluate_member_access_f096,
    FindingEnum.F063: evaluate_member_access_f063,
    FindingEnum.F098: evaluate_member_access_f098,
    FindingEnum.F100: evaluate_member_access_f100,
    FindingEnum.F239: evaluate_member_access_f239,
    FindingEnum.F413: evaluate_member_access_f413,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    args.evaluation[args.n_id] = args.generic(args.fork_n_id(expr_id)).danger
    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
