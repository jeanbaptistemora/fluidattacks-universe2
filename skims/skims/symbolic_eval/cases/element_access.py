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
    acces_attr = args.graph.nodes[args.n_id]
    d_arguments = args.generic(args.fork_n_id(acces_attr["arguments_id"]))
    d_expression = args.generic(args.fork_n_id(acces_attr["expression_id"]))

    args.graph.nodes[args.n_id]["danger"] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return args.graph.nodes[args.n_id]["danger"]
