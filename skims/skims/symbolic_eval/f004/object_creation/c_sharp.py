# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_OBJ = {"StreamReader", "SqlCommand"}


def cs_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "Executor":
        args.triggers.add("Executor")
    elif args.graph.nodes[args.n_id]["name"] in DANGER_OBJ:
        args.triggers.add("UserConnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
