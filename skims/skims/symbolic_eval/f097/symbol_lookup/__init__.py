from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f097.symbol_lookup.javascript import (
    javascript_has_reverse_tabnabbing,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_HAS_REVERSE_TABNABBING: javascript_has_reverse_tabnabbing,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
