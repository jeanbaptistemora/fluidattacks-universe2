# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["member"] in {"QueryString"}:
        args.triggers.add("UserParams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
