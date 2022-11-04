# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_jwt_token(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    value = args.graph.nodes[args.n_id]["value"][1:-1].lower()
    if value in {"none", "hs256"}:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
