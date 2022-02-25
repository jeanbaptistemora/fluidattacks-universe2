from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f021.object_creation import (
    evaluate as evaluate_parameter_f021,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F021: evaluate_parameter_f021,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    args.evaluation[args.n_id] = False

    if al_id := args.graph.nodes[args.n_id].get("arguments_id"):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(al_id))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
