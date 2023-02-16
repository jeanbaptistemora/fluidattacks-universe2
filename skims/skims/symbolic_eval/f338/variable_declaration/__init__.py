from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f338.variable_declaration.common import (
    variable_is_harcoded,
)
from symbolic_eval.f338.variable_declaration.go import (
    go_variable_is_harcoded,
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
    MethodsEnum.TS_SALT_IS_HARDCODED: variable_is_harcoded,
    MethodsEnum.JS_SALT_IS_HARDCODED: variable_is_harcoded,
    MethodsEnum.JAVA_SALT_IS_HARDCODED: variable_is_harcoded,
    MethodsEnum.KOTLIN_SALT_IS_HARDCODED: variable_is_harcoded,
    MethodsEnum.GO_SALT_IS_HARDCODED: go_variable_is_harcoded,
    MethodsEnum.DART_SALT_IS_HARDCODED: variable_is_harcoded,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
