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
    block_id = args.graph.nodes[args.n_id]["block_id"]
    block_danger = args.generic(args.fork_n_id(block_id)).danger

    if pl_id := args.graph.nodes[args.n_id].get("parameters_id"):
        params_danger = args.generic(args.fork_n_id(pl_id)).danger

    args.evaluation[args.n_id] = block_danger or params_danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
