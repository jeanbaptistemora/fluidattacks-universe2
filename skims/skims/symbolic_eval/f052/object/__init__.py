from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.object.common import (
    insecure_encrypt,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_ENCRYPT: insecure_encrypt,
    MethodsEnum.TS_INSECURE_ENCRYPT: insecure_encrypt,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
