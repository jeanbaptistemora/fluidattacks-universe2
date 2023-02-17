from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f091.method_invocation.java import (
    java_insecure_logging,
)
from symbolic_eval.f091.method_invocation.javascript import (
    javascript_insecure_logging,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_INSECURE_LOGGING: java_insecure_logging,
    MethodsEnum.JS_INSECURE_LOGGING: javascript_insecure_logging,
    MethodsEnum.TS_INSECURE_LOGGING: javascript_insecure_logging,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
