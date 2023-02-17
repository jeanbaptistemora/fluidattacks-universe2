from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f004.object_creation.c_sharp import (
    cs_remote_command_execution,
)
from symbolic_eval.f004.object_creation.java import (
    java_remote_command_execution,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_REMOTE_COMMAND_EXECUTION: cs_remote_command_execution,
    MethodsEnum.JAVA_REMOTE_COMMAND_EXECUTION: java_remote_command_execution,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
