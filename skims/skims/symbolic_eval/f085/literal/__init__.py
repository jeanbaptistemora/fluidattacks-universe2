from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f085.literal.javascript import (
    client_storage,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_CLIENT_STORAGE: client_storage,
    MethodsEnum.TS_CLIENT_STORAGE: client_storage,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
