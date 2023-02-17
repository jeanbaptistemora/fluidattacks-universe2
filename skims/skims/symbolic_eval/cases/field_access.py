from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f052.field_access import (
    evaluate as evaluate_field_access_f052,
)
from symbolic_eval.f350.field_access import (
    evaluate as evaluate_field_access_f350,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F052: evaluate_field_access_f052,
    FindingEnum.F350: evaluate_field_access_f350,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
