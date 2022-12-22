from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f021.member_access.c_sharp import (
    cs_insec_addheader_write,
    cs_xpath_injection,
)
from symbolic_eval.f021.member_access.common import (
    dynamic_xpath,
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
    MethodsEnum.CS_XPATH_INJECTION: cs_xpath_injection,
    MethodsEnum.CS_XPATH_INJECTION_EVALUATE: cs_insec_addheader_write,
    MethodsEnum.JS_DYNAMIC_X_PATH: dynamic_xpath,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
