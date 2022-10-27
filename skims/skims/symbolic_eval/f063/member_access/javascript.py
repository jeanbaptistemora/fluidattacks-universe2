# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_path_traversal(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "resolve":
        args.triggers.add("resolve")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
