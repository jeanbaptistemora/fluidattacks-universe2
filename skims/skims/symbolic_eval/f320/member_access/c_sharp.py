# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_ldap_authenticated(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    insecure_types = {"None", "Anonymous"}
    if args.graph.nodes[args.n_id]["member"] in insecure_types:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
