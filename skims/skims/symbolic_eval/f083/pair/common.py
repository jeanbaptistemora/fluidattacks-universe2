# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def generic_xml_parser(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attr = args.graph.nodes[args.n_id]
    if (
        args.graph.nodes[n_attr["key_id"]].get("symbol") == "noent"
        and args.graph.nodes[n_attr["value_id"]].get("value") == "true"
    ):
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
