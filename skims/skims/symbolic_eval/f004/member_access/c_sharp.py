# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    string,
)


def cs_remote_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = (
        ma_attr["expression"]
        in string.build_attr_paths("System.Diagnostics.Process")
        and ma_attr["member"] == "Start"
    ) or ma_attr["member"] == "Execute"
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
