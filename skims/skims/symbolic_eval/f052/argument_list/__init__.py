from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.argument_list.kotlin import (
    kt_insecure_certification,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.KT_INSECURE_CERTIFICATE_VALIDATION: kt_insecure_certification,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
