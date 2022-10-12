# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_host_key_checking(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"].replace('"', "").lower() == "no":
        args.triggers.add("no")
    if (
        args.graph.nodes[args.n_id]["value"].replace('"', "").lower()
        == "stricthostkeychecking"
    ):
        args.triggers.add("hostkey")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
