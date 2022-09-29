# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "QueryString",
    "ReadLine",
    "GetString",
    "Cookies",
    "FileName",
}


def cs_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["member"] in DANGER_METHODS or (
        "params.get" in f'{ma_attr["expression"]}.{ma_attr["member"]}'.lower()
    ):
        args.triggers.add("UserParams")
    elif ma_attr["member"] == "GetEnvironmentVariable":
        args.triggers.update({"UserParams", "UserConnection"})

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
