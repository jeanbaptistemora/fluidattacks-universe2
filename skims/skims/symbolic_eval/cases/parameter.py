from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f008.cases.parameter import (
    evaluate as evaluate_parameter,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F008: evaluate_parameter,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return args.graph.nodes[args.n_id]["danger"]
