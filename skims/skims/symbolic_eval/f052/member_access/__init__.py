# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.member_access.c_sharp import (
    cs_managed_secure_mode,
)
from symbolic_eval.f052.member_access.javascript import (
    js_insecure_cipher,
)
from symbolic_eval.f052.member_access.typescript import (
    tsx_insecure_aes_cipher,
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
    MethodsEnum.CS_MANAGED_SECURE_MODE: cs_managed_secure_mode,
    MethodsEnum.JS_INSECURE_CIPHER: js_insecure_cipher,
    MethodsEnum.TSX_INSECURE_AES_CIPHER: tsx_insecure_aes_cipher,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
