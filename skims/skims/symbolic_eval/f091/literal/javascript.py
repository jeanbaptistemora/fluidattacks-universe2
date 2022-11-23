# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def javascript_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    sanitize = {
        '"[\\n\\r\\t]"',
        "/\\n|\\r/g",
    }
    print(args.graph.nodes[args.n_id]["value"])
    if args.graph.nodes[args.n_id]["value"] in sanitize:
        args.triggers.add("characters")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
