from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f211.parameter.c_sharp import (
    cs_regex_injection,
    cs_vuln_regex,
)
from symbolic_eval.f211.parameter.java import (
    java_vuln_regex,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_REGEX_INJETCION: cs_regex_injection,
    MethodsEnum.CS_VULN_REGEX: cs_vuln_regex,
    MethodsEnum.JAVA_VULN_REGEX: java_vuln_regex,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
