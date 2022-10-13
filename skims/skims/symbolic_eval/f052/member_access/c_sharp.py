# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_managed_secure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    unsafe_modes = {
        "CipherMode.ECB",
        "CipherMode.OFB",
        "CipherMode.CFB",
        "CipherMode.CBC",
    }

    node = args.graph.nodes[args.n_id]
    if f'{node["expression"]}.{node["member"]}' in unsafe_modes:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
