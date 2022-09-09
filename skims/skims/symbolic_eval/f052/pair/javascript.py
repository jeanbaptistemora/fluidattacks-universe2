# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    pair_node = args.graph.nodes[args.n_id]
    key = pair_node["key_id"]
    value = pair_node["value_id"]
    if (symbol := args.graph.nodes[key].get("symbol")) and symbol in {
        "mode",
        "padding",
    }:
        if len(args.triggers) == 0:
            args.triggers.add(symbol)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + "." + symbol)
        args.generic(args.fork_n_id(value))

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def js_insecure_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    pair_node = args.graph.nodes[args.n_id]
    key = pair_node["key_id"]
    value = pair_node["value_id"]
    if args.graph.nodes[key]["symbol"] == "modulusLength":
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(value)).danger
    elif args.graph.nodes[key]["symbol"] == "namedCurve":
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(value)).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
