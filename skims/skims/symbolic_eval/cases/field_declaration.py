from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if v_id := g.match_ast_d(args.graph, args.n_id, "VariableDeclaration"):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(v_id)).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
