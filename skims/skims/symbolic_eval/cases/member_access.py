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
    graph = args.graph
    mem_expr = args.n_id

    expr_id = graph.nodes[mem_expr]["expression_id"]
    graph.nodes[mem_expr]["danger"] = args.generic(args.fork_n_id(expr_id))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[mem_expr]["danger"] = finding_evaluator(args)

    return graph.nodes[mem_expr]["danger"]
