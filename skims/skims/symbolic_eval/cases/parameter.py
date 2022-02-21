from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f008.parameter import (
    evaluate as evaluate_parameter_f008,
)
from symbolic_eval.f100.parameter import (
    evaluate as evaluate_parameter_f100,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F008: evaluate_parameter_f008,
    FindingEnum.F100: evaluate_parameter_f100,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    args.evaluation[args.n_id] = False

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
