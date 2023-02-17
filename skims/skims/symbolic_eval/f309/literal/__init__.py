from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f309.literal.common import (
    insecure_jwt_token,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_JWT_TOKEN: insecure_jwt_token,
    MethodsEnum.TS_INSECURE_JWT_TOKEN: insecure_jwt_token,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
