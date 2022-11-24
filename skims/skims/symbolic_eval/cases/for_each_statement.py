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
    iterable_id = args.graph.nodes[args.n_id]["iterable_item_id"]
    args.evaluation[args.n_id] = args.generic(
        args.fork_n_id(iterable_id)
    ).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
