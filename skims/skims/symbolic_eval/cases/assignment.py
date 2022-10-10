# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    op_attr = args.graph.nodes[args.n_id]
    var_id = op_attr["variable_id"]

    if args.graph.nodes[var_id]["label_type"] == "MemberAccess":
        d_var = args.generic(args.fork_n_id(var_id)).danger
    else:
        d_var = False

    d_value = args.generic(args.fork_n_id(op_attr["value_id"])).danger

    args.evaluation[args.n_id] = d_var or d_value

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
