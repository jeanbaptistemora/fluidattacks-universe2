# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "replaceAll":
        args.triggers.add("replaceAll")
    elif args.graph.nodes[args.n_id]["expression"] == "getParameter":
        args.evaluation[args.n_id] = args.generic(
            args.fork_n_id(args.graph.nodes[args.n_id].get("object_id"))
        ).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
