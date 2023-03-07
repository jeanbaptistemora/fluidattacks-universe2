from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.member_access.c_sharp import (
    cs_managed_secure_mode,
)
from symbolic_eval.f052.member_access.common import (
    insecure_mode,
)
from symbolic_eval.f052.member_access.kotlin import (
    kt_insecure_cipher_http,
    kt_insecure_init_vector,
)
from symbolic_eval.f052.member_access.python import (
    python_unsafe_ciphers,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_MANAGED_SECURE_MODE: cs_managed_secure_mode,
    MethodsEnum.JS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.TS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.KT_INSECURE_CIPHER_HTTP: kt_insecure_cipher_http,
    MethodsEnum.PYTHON_UNSAFE_CIPHER: python_unsafe_ciphers,
    MethodsEnum.KT_INSECURE_INIT_VECTOR: kt_insecure_init_vector,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
