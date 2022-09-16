# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f034.call_expression import (
    evaluate as evaluate_call_expression_f034,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F034: evaluate_call_expression_f034,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    al_id = args.graph.nodes[args.n_id]["arguments_id"]
    d_arguments = args.generic(args.fork_n_id(al_id)).danger

    if expr_id := args.graph.nodes[args.n_id].get("expression_id"):
        d_expression = args.generic(args.fork_n_id(expr_id)).danger
    else:
        d_expression = False

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
