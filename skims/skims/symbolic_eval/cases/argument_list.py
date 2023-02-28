from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f153.argument_list import (
    evaluate as evaluate_argument_list_f153,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F153: evaluate_argument_list_f153,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    arg_ids = g.adj_ast(args.graph, args.n_id)
    danger = [
        args.generic(args.fork_n_id(arg_id)).danger for arg_id in arg_ids
    ]
    args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
