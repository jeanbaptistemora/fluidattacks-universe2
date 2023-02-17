from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f211.method_invocation.common import (
    common_regex_injection,
)
from symbolic_eval.f211.method_invocation.java import (
    java_vuln_regex,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_VULN_REGEX: java_vuln_regex,
    MethodsEnum.JS_REGEX_INJETCION: common_regex_injection,
    MethodsEnum.TS_REGEX_INJETCION: common_regex_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
