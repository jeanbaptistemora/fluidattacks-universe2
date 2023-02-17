from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f343.method_declaration import (
    evaluate as evaluate_method_declaration_f343,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F343: evaluate_method_declaration_f343,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    danger_params = False
    if pl_id := args.graph.nodes[args.n_id].get("parameters_id"):
        danger_params = args.generic(args.fork_n_id(pl_id)).danger
    danger_block = False
    if block_id := args.graph.nodes[args.n_id].get("block_id"):
        danger_block = args.generic(args.fork_n_id(block_id)).danger

    args.evaluation[args.n_id] = danger_params or danger_block
    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
