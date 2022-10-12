# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    string,
)


def java_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    lib = string.build_attr_paths(
        "javax", "servlet", "http", "HttpServletRequest"
    )

    if args.graph.nodes[args.n_id]["variable_type"] in lib:
        args.triggers.add("HttpServletRequest")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
