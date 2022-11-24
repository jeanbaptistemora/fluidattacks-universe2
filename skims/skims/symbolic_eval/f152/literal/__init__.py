from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f152.literal.typescript import (
    insecure_http_headers,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

METHOD_EVALUATORS: Dict[MethodsEnum, Evaluator] = {
    MethodsEnum.TS_UNSAFE_HTTP_X_FRAME_OPTIONS: insecure_http_headers,
    MethodsEnum.JS_UNSAFE_HTTP_X_FRAME_OPTIONS: insecure_http_headers,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
