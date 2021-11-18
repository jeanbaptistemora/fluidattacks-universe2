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
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    arg_ids = g.adj_ast(args.graph, args.n_id)
    danger = [args.generic(args.fork_n_id(arg_id)) for arg_id in arg_ids]
    args.graph.nodes[args.n_id]["danger"] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return args.graph.nodes[args.n_id]["danger"]
