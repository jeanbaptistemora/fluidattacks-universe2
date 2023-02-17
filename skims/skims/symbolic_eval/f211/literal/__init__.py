from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f211.literal.c_sharp import (
    cs_vuln_regex,
)
from symbolic_eval.f211.literal.java import (
    java_vuln_regex,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_VULN_REGEX: cs_vuln_regex,
    MethodsEnum.JAVA_VULN_REGEX: java_vuln_regex,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
