from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f135.literal.typescript import (
    insecure_http_headers,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.TS_UNSAFE_HTTP_XSS_PROTECTION: insecure_http_headers,
    MethodsEnum.JS_UNSAFE_HTTP_XSS_PROTECTION: insecure_http_headers,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
