# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_type_name_handling(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    args.evaluation[args.n_id] = member_access == "TypeNameHandling.All"
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_xml_serial(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'

    if member_access == "Type.GetType":
        args.evaluation[args.n_id] = True
        args.triggers.add(member_access)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
