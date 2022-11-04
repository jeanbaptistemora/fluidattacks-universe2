# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.common import (
    INSECURE_ALGOS,
    INSECURE_MODES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_create_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        cipher = args.graph.nodes[args.n_id]["value"][1:-1].lower().split("-")
        args.evaluation[args.n_id] = any(
            mode in cipher for mode in INSECURE_MODES
        ) or any(algo in cipher for algo in INSECURE_ALGOS)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
