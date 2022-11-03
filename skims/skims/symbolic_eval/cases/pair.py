# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f083.pair import (
    evaluate as evaluate_literal_f083,
)
from symbolic_eval.f309.pair import (
    evaluate as evaluate_literal_f309,
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
    FindingEnum.F083: evaluate_literal_f083,
    FindingEnum.F309: evaluate_literal_f309,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attr = args.graph.nodes[args.n_id]
    key_danger = args.generic(args.fork_n_id(n_attr["key_id"])).danger
    val_danger = args.generic(args.fork_n_id(n_attr["value_id"])).danger

    args.evaluation[args.n_id] = key_danger or val_danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
