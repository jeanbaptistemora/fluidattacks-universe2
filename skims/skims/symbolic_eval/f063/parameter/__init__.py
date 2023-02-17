from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f063.parameter.c_sharp import (
    cs_open_redirect,
    cs_unsafe_path_traversal,
)
from symbolic_eval.f063.parameter.java import (
    java_unsafe_path_traversal,
    java_zip_slip_injection,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_OPEN_REDIRECT: cs_open_redirect,
    MethodsEnum.CS_UNSAFE_PATH_TRAVERSAL: cs_unsafe_path_traversal,
    MethodsEnum.JAVA_ZIP_SLIP_PATH_INJECTION: java_zip_slip_injection,
    MethodsEnum.JAVA_UNSAFE_PATH_TRAVERSAL: java_unsafe_path_traversal,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
