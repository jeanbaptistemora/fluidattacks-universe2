from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f008.literal.common import (
    unsafe_xss_content,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_UNSAFE_XSS_CONTENT: unsafe_xss_content,
    MethodsEnum.TS_UNSAFE_XSS_CONTENT: unsafe_xss_content,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
