from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f297.variable_declaration import (
    evaluate as evaluate_variable_declaration_f297,
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
    FindingEnum.F297: evaluate_variable_declaration_f297,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if val_id := args.graph.nodes[args.n_id].get("value_id"):
        args.evaluation[args.n_id] = args.generic(
            args.fork_n_id(val_id)
        ).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
