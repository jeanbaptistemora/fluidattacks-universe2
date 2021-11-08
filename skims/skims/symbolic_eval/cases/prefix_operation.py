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
    op_attr = args.graph.nodes[args.n_id]
    op_attr["danger"] = args.generic(args.fork_n_id(op_attr["expression_id"]))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        op_attr["danger"] = finding_evaluator(args)

    return op_attr["danger"]
