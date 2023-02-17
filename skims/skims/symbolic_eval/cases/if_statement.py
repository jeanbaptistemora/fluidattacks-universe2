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
    danger_cond = False
    danger_true = False
    danger_false = False
    node = args.graph.nodes[args.n_id]
    if _id := node.get("condition_id"):
        danger_cond = args.generic(args.fork_n_id(_id)).danger
    if args.n_id not in args.path:
        if _id := node.get("true_id"):
            danger_true = args.generic(args.fork_n_id(_id)).danger
        if _id := node.get("false_id"):
            danger_false = args.generic(args.fork_n_id(_id)).danger

    args.evaluation[args.n_id] = danger_cond or danger_true or danger_false

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
