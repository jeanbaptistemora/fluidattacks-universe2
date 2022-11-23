# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

requests = {
    "query",
    "req",
}


def js_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if "query" in args.graph.nodes[args.n_id]["member"]:
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
