from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f004.member_access.c_sharp import (
    cs_remote_command_execution,
)
from symbolic_eval.f004.member_access.common import (
    remote_command_execution,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_REMOTE_COMMAND_EXECUTION: cs_remote_command_execution,
    MethodsEnum.JS_REMOTE_COMMAND_EXECUTION: remote_command_execution,
    MethodsEnum.TS_REMOTE_COMMAND_EXECUTION: remote_command_execution,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
