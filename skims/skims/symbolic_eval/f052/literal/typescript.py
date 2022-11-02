# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_MODES = {"ecb", "ofb", "cfb", "cbc"}

DANGER_ALGOS = {"blowfish", "bf", "des", "desede", "rc2", "rc4", "rsa"}


def ts_insecure_create_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        cipher = args.graph.nodes[args.n_id]["value"][1:-1].lower().split("-")
        args.evaluation[args.n_id] = any(
            mode in cipher for mode in DANGER_MODES
        ) or any(algo in cipher for algo in DANGER_ALGOS)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)