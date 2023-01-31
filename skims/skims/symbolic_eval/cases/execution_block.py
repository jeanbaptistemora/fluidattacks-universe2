from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    NId,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
    List,
    Tuple,
    Union,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    danger_nodes: Union[List[NId], Tuple]
    if args.n_id in args.path:
        danger_nodes = args.path[: args.path.index(args.n_id)]
    else:
        danger_nodes = g.adj_ast(args.graph, args.n_id)

    danger = [
        args.generic(args.fork_n_id(arg_id)).danger for arg_id in danger_nodes
    ]
    args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
