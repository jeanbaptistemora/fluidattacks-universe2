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
    expr = node["expression"].replace(".", "")
    if memb in {"mode", "pad"}:
        if len(args.triggers) == 0:
            args.triggers.add(expr)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + "." + expr)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
