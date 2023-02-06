from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f344.method_invocation.common import (
    js_ls_sensitive_data,
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
    MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_ASYNC: js_ls_sensitive_data,
    MethodsEnum.TS_LOCAL_STORAGE_SENS_DATA_ASYNC: js_ls_sensitive_data,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)