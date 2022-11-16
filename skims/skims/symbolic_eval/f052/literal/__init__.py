# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.literal.c_sharp import (
    cs_disabled_strong_crypto,
    cs_insecure_keys,
    cs_rsa_secure_mode,
)
from symbolic_eval.f052.literal.common import (
    insecure_create_cipher,
)
from symbolic_eval.f052.literal.java import (
    java_evaluate_cipher,
    java_insecure_cipher_jmqi,
    java_insecure_cipher_ssl,
    java_insecure_hash,
    java_insecure_key_ec,
    java_insecure_key_rsa,
)
from symbolic_eval.f052.literal.javascript import (
    js_insecure_ecdh_key,
    js_insecure_hash,
    js_insecure_key,
    js_insecure_key_pair,
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
    MethodsEnum.JAVA_INSECURE_KEY_EC: java_insecure_key_ec,
    MethodsEnum.JAVA_INSECURE_KEY_RSA: java_insecure_key_rsa,
    MethodsEnum.JAVA_INSECURE_KEY_SECRET: java_evaluate_cipher,
    MethodsEnum.JAVA_INSECURE_HASH: java_insecure_hash,
    MethodsEnum.JAVA_INSECURE_CIPHER: java_evaluate_cipher,
    MethodsEnum.JAVA_INSECURE_CIPHER_SSL: java_insecure_cipher_ssl,
    MethodsEnum.JAVA_INSECURE_CIPHER_JMQI: java_insecure_cipher_jmqi,
    MethodsEnum.JS_INSECURE_HASH: js_insecure_hash,
    MethodsEnum.TS_INSECURE_HASH: js_insecure_hash,
    MethodsEnum.JS_INSECURE_CREATE_CIPHER: insecure_create_cipher,
    MethodsEnum.JS_INSECURE_ECDH_KEY: js_insecure_ecdh_key,
    MethodsEnum.TS_INSECURE_ECDH_KEY: js_insecure_ecdh_key,
    MethodsEnum.JS_INSECURE_EC_KEYPAIR: js_insecure_key_pair,
    MethodsEnum.JS_INSECURE_RSA_KEYPAIR: js_insecure_key_pair,
    MethodsEnum.JS_INSECURE_KEY: js_insecure_key,
    MethodsEnum.TS_INSECURE_CREATE_CIPHER: insecure_create_cipher,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
