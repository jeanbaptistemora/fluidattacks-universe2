# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_authentication(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "HttpHeaders":
        args.evaluation[args.n_id] = True
        args.triggers.add("ObjectCreation")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
