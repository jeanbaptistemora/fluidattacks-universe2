from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f343.method_declaration import (
    evaluate as evaluate_method_declaration_f343,
)
from symbolic_eval.f344.method_declaration import (
    evaluate as evaluate_method_declaration_f344,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F343: evaluate_method_declaration_f343,
    FindingEnum.F344: evaluate_method_declaration_f344,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if pl_id := args.graph.nodes[args.n_id].get("parameters_id"):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(pl_id)).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
