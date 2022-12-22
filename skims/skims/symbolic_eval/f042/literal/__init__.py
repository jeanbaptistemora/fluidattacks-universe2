from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f042.literal.c_sharp import (
    cs_insecure_cookies,
)
from symbolic_eval.f042.literal.java import (
    java_insecure_cookie,
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
    MethodsEnum.CS_INSEC_COOKIES: cs_insecure_cookies,
    MethodsEnum.JAVA_INSECURE_COOKIE: java_insecure_cookie,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
