from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    args.evaluation[args.n_id] = False

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
