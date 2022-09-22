# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_sql_user_params(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["member"] == "CommandText":
        args.triggers.add("CommandText")
    elif ma_attr["member"] in {"ReadLine", "GetString", "Cookies"}:
        args.triggers.add("UserParams")
    elif (
        "params.get" in f'{ma_attr["expression"]}.{ma_attr["member"]}'.lower()
    ):
        args.triggers.add("UserParams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
