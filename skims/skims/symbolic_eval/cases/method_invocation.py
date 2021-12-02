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
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    a_id = args.graph.nodes[args.n_id]["arguments_id"]

    d_expression = args.generic(args.fork_n_id(expr_id))
    d_arguments = args.generic(args.fork_n_id(a_id))

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
