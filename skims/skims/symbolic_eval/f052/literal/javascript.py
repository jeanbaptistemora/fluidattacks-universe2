# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.common import (
    INSECURE_HASHES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if any(hash in member_str.lower() for hash in INSECURE_HASHES):
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def js_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"].replace('"', "")
        if len(args.triggers) == 0:
            args.triggers.add(member_str)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + member_str)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def js_insecure_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] in {"string", "number"}:
        value = args.graph.nodes[args.n_id]["value"].replace('"', "")
        args.triggers.clear()
        args.triggers.add(value)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
