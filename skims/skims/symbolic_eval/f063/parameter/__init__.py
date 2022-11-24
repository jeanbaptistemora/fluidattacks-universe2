from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f063.parameter.c_sharp import (
    cs_open_redirect,
)
from symbolic_eval.f063.parameter.java import (
    java_zip_slip_injection,
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
    MethodsEnum.CS_OPEN_REDIRECT: cs_open_redirect,
    MethodsEnum.JAVA_ZIP_SLIP_PATH_INJECTION: java_zip_slip_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
