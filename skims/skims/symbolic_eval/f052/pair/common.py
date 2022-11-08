# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if args.graph.nodes[key].get("symbol") == "mode":
        val_danger = args.generic(args.fork(n_id=value)).danger
        if val_danger:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_key_pair(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    key_name = args.graph.nodes[key].get("symbol")

    if key_name and key_name.lower() == "moduluslength":
        if args.generic(args.fork(n_id=value)).danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("unsafemodulus")

    if key_name and key_name.lower() == "namedcurve":
        if args.generic(args.fork(n_id=value)).danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("unsafecurve")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
