from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f063.member_access.c_sharp import (
    cs_open_redirect,
    cs_unsafe_path_traversal,
)
from symbolic_eval.f063.member_access.common import (
    insecure_path_traversal,
    zip_slip,
)
from symbolic_eval.f063.member_access.python import (
    python_path_traversal,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_OPEN_REDIRECT: cs_open_redirect,
    MethodsEnum.CS_UNSAFE_PATH_TRAVERSAL: cs_unsafe_path_traversal,
    MethodsEnum.JS_PATH_TRAVERSAL: insecure_path_traversal,
    MethodsEnum.JS_ZIP_SLIP: zip_slip,
    MethodsEnum.PYTHON_IO_PATH_TRAVERSAL: python_path_traversal,
    MethodsEnum.TS_PATH_TRAVERSAL: insecure_path_traversal,
    MethodsEnum.TS_ZIP_SLIP: zip_slip,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
