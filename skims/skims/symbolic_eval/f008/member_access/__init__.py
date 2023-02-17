from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f008.member_access.c_sharp import (
    cs_insec_addheader_write,
)
from symbolic_eval.f008.member_access.common import (
    unsafe_xss_content,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSEC_ADDHEADER_WRITE: cs_insec_addheader_write,
    MethodsEnum.JS_UNSAFE_XSS_CONTENT: unsafe_xss_content,
    MethodsEnum.TS_UNSAFE_XSS_CONTENT: unsafe_xss_content,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
