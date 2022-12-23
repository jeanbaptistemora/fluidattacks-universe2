from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f112.member_access.common import (
    unsafe_sql_injection,
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
    MethodsEnum.JS_SQL_API_INJECTION: unsafe_sql_injection,
    MethodsEnum.TS_SQL_API_INJECTION: unsafe_sql_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
