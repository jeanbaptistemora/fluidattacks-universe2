from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.literal.c_sharp import (
    cs_disabled_strong_crypto,
    cs_insecure_keys,
    cs_rsa_secure_mode,
)
from symbolic_eval.f052.literal.java import (
    java_insecure_key,
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
    MethodsEnum.CS_DISABLED_STRONG_CRYPTO: cs_disabled_strong_crypto,
    MethodsEnum.CS_INSECURE_KEYS: cs_insecure_keys,
    MethodsEnum.CS_RSA_SECURE_MODE: cs_rsa_secure_mode,
    MethodsEnum.JAVA_INSECURE_KEY: java_insecure_key,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
