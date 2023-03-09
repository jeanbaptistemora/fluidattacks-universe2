from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.method_invocation.kotlin import (
    kt_insec_key_gen,
    kt_insecure_cert,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.KT_INSECURE_CERTIFICATE_VALIDATION: kt_insecure_cert,
    MethodsEnum.KT_INSECURE_KEY_GEN: kt_insec_key_gen,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
