from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f134.literal import (
    evaluate as evaluate_literal_f134,
)
from symbolic_eval.f239.literal import (
    evaluate as evaluate_literal_f239,
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
    FindingEnum.F134: evaluate_literal_f134,
    FindingEnum.F239: evaluate_literal_f239,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
