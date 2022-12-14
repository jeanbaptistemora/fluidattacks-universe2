from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f192.method_invocation.common import (
    common_reflected_xss,
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
    MethodsEnum.JS_REFLECTED_XSS: common_reflected_xss,
    MethodsEnum.TS_REFLECTED_XSS: common_reflected_xss,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
