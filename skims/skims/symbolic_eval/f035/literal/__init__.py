from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f035.literal.c_sharp import (
    cs_no_password,
    cs_weak_credential,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_NO_PASSWORD: cs_no_password,
    MethodsEnum.CS_WEAK_CREDENTIAL: cs_weak_credential,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
