# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "getBytes",
    "getHeader",
    "getHeaderNames",
    "getHeaders",
    "getName",
    "getParameter",
    "getParameterMap",
    "getParameterNames",
    "getParameterValues",
    "getQueryString",
    "getValue",
}


def java_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    m_attr = args.graph.nodes[args.n_id]
    if m_attr["expression"] == "replaceAll":
        args.triggers.add("sanitized")

    if m_attr["expression"] in DANGER_METHODS:
        args.triggers.add("userparams")

    if obj_id := m_attr.get("object_id"):
        args.evaluation[args.n_id] = args.generic(
            args.fork_n_id(obj_id)
        ).danger
    else:
        args.evaluation[args.n_id] = False

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
