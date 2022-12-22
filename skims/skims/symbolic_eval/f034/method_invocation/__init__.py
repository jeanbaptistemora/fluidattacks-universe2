from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f034.method_invocation.java import (
    java_weak_random,
)
from symbolic_eval.f034.method_invocation.javascript import (
    weak_random,
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
    MethodsEnum.JAVA_WEAK_RANDOM_COOKIE: java_weak_random,
    MethodsEnum.JS_WEAK_RANDOM: weak_random,
    MethodsEnum.TS_WEAK_RANDOM: weak_random,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
