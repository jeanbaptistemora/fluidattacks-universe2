# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.common import (
    check_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_open_redirect(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = check_http_inputs(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
