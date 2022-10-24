# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_authentication(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "getHeaders":
        args.evaluation[args.n_id] = True
        args.triggers.add("getHeaders")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
