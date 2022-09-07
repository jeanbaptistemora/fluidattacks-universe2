# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_no_password(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    if str_value := str(args.graph.nodes[args.n_id]["value"])[1:-1]:
        if len(args.triggers) == 0:
            args.triggers.add(str_value)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + str_value)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_weak_credential(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    args.triggers.add(args.graph.nodes[args.n_id]["value"])

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
