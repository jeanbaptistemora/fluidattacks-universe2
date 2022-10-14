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
    block_id = args.graph.nodes[args.n_id]["block_id"]
    block_danger = args.generic(args.fork_n_id(block_id)).danger

    if pl_id := args.graph.nodes[args.n_id].get("parameters_id"):
        params_danger = args.generic(args.fork_n_id(pl_id)).danger

    args.evaluation[args.n_id] = block_danger or params_danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
