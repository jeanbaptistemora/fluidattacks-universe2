from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.object.common import (
    insecure_encrypt,
    insecure_sign,
)
from symbolic_eval.f052.object.kotlin import (
    kt_insecure_cert,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_ENCRYPT: insecure_encrypt,
    MethodsEnum.TS_INSECURE_ENCRYPT: insecure_encrypt,
    MethodsEnum.JS_JWT_INSEC_SIGN_ALGORITHM: insecure_sign,
    MethodsEnum.TS_JWT_INSEC_SIGN_ALGORITHM: insecure_sign,
    MethodsEnum.KT_INSECURE_CERTIFICATE_VALIDATION: kt_insecure_cert,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
