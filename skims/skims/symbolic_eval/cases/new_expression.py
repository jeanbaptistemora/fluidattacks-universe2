from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    c_danger = args.generic(args.fork_n_id(n_attrs["constructor_id"])).danger
    if al_id := n_attrs.get("arguments_id"):
        al_danger = args.generic(args.fork_n_id(al_id)).danger
    else:
        al_danger = False

    args.evaluation[args.n_id] = c_danger or al_danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
