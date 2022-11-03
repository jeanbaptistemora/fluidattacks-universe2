# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.common import (
    INSECURE_ALGOS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_uses_insecure_jwt_token(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    value = args.graph.nodes[args.n_id]["value"][1:-1].lower()
    if value in INSECURE_ALGOS:
        args.evaluation[args.n_id] = True
        args.triggers.add("unsafealgo")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
