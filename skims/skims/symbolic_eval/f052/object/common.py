# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def insecure_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    for pair_id in g.match_ast_group_d(args.graph, args.n_id, "Pair"):
        pair_node = args.graph.nodes[pair_id]
        key = pair_node["key_id"]
        value = pair_node["value_id"]
        if (
            args.graph.nodes[key]["symbol"] == "modulusLength"
            or args.graph.nodes[key]["symbol"] == "namedCurve"
        ):
            args.triggers.clear()
            args.triggers.update(
                args.generic(
                    args.fork(n_id=value, evaluation={}, triggers=set())
                ).triggers
            )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_encrypt(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    obj_keys = []
    for pair_id in g.match_ast_group_d(args.graph, args.n_id, "Pair"):
        pair_node = args.graph.nodes[pair_id]
        key = pair_node["key_id"]
        obj_keys.append(args.graph.nodes[key]["symbol"])

    if not any(key == "mode" for key in obj_keys):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
