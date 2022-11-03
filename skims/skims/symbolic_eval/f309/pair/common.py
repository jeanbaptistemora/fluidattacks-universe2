# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_jwt_token(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    args.triggers.clear()
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if args.graph.nodes[key]["symbol"].lower() in {"algorithm", "algorithms"}:
        args.evaluation[args.n_id] = True
        args.triggers.update(
            args.generic(
                args.fork(n_id=value, evaluation={}, triggers=set())
            ).triggers
        )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
