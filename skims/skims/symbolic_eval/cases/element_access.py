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
    acces_attr = args.graph.nodes[args.n_id]
    d_arguments = args.generic(
        args.fork_n_id(acces_attr["arguments_id"])
    ).danger
    d_expression = args.generic(
        args.fork_n_id(acces_attr["expression_id"])
    ).danger

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
