from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f344.object_creation.common import (
    js_ls_sensitive_data,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA: js_ls_sensitive_data,
    MethodsEnum.TS_LOCAL_STORAGE_WITH_SENSITIVE_DATA: js_ls_sensitive_data,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
