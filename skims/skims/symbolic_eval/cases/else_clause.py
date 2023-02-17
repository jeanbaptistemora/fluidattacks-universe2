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
    child_labels = {"block_id"}
    for label in child_labels:
        if n_id := args.graph.nodes[args.n_id].get(label):
            args.evaluation[args.n_id] = args.generic(
                args.fork_n_id(n_id)
            ).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
