from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f004.parameter import (
    evaluate as evaluate_parameter_f004,
)
from symbolic_eval.f008.parameter import (
    evaluate as evaluate_parameter_f008,
)
from symbolic_eval.f021.parameter import (
    evaluate as evaluate_parameter_f021,
)
from symbolic_eval.f100.parameter import (
    evaluate as evaluate_parameter_f100,
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
    FindingEnum.F004: evaluate_parameter_f004,
    FindingEnum.F008: evaluate_parameter_f008,
    FindingEnum.F021: evaluate_parameter_f021,
    FindingEnum.F100: evaluate_parameter_f100,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
