# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f091.member_access.c_sharp import (
    cs_insecure_logging,
)
from symbolic_eval.f091.member_access.javascript import (
    js_insecure_logging,
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
    MethodsEnum.CS_INSECURE_LOGGING: cs_insecure_logging,
    MethodsEnum.JS_INSECURE_LOGGING: js_insecure_logging,
    MethodsEnum.TS_INSECURE_LOGGING: js_insecure_logging,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
