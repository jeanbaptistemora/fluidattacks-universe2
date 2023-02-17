from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f042.pair.common import (
    js_insecure_cookie,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSEC_COOKIES: js_insecure_cookie,
    MethodsEnum.TS_INSEC_COOKIES: js_insecure_cookie,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
