# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_client_storage(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.triggers.add(args.graph.nodes[args.n_id]["value"])
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
