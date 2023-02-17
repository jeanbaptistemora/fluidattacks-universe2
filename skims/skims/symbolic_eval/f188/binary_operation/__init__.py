from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f188.binary_operation.common import (
    has_origin_check,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.TSX_LACK_OF_VALIDATION_EVENT_LISTENER: has_origin_check,
    MethodsEnum.JSX_LACK_OF_VALIDATION_EVENT_LISTENER: has_origin_check,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
