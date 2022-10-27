# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_MODES = {"ecb", "ofb", "cfb", "cbc"}


def ts_insecure_aes_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    node = args.graph.nodes[args.n_id]

    if (
        node["member"].lower() == "cryptojs.mode"
        and node["expression"].lower() in DANGER_MODES
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)