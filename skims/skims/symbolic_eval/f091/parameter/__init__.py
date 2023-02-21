from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f091.parameter.c_sharp import (
    cs_insecure_logging,
)
from symbolic_eval.f091.parameter.dart import (
    dart_insecure_logging,
)
from symbolic_eval.f091.parameter.java import (
    java_insecure_logging,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSECURE_LOGGING: cs_insecure_logging,
    MethodsEnum.JAVA_INSECURE_LOGGING: java_insecure_logging,
    MethodsEnum.DART_INSECURE_LOGGING: dart_insecure_logging,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
