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
    if_attr = args.graph.nodes[args.n_id]
    if_attr["danger"] = args.generic(args.fork_n_id(if_attr["condition_id"]))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        if_attr["danger"] = finding_evaluator(args)

    return if_attr["danger"]
