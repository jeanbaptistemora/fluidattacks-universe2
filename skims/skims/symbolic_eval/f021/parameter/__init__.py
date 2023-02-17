from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f021.parameter.c_sharp import (
    cs_xpath_injection,
    cs_xpath_injection_evaluate,
)
from symbolic_eval.f021.parameter.java import (
    java_xpath_injection_evaluate,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_XPATH_INJECTION: cs_xpath_injection,
    MethodsEnum.CS_XPATH_INJECTION_EVALUATE: cs_xpath_injection_evaluate,
    MethodsEnum.JAVA_XPATH_INJECTION_EVALUATE: java_xpath_injection_evaluate,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
