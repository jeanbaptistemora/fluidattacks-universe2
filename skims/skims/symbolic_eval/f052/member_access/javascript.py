# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    node = args.graph.nodes[args.n_id]
    memb = node["member"].split(".")[-1].lower()
    expr = node["expression"]
    if memb == "mode":
        args.triggers.clear()
        args.triggers.add(expr)
    elif memb == "pad":
        args.triggers.clear()
        args.triggers.add(expr)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
