# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_weak_random(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if "Math.random()" in args.graph.nodes[args.n_id]["expression"]:
        args.triggers.add("Random")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
