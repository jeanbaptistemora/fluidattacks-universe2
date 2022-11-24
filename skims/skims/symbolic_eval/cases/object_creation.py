from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f001.object_creation import (
    evaluate as evaluate_parameter_f001,
)
from symbolic_eval.f004.object_creation import (
    evaluate as evaluate_parameter_f004,
)
from symbolic_eval.f015.object_creation import (
    evaluate as evaluate_parameter_f015,
)
from symbolic_eval.f016.object_creation import (
    evaluate as evaluate_parameter_f016,
)
from symbolic_eval.f021.object_creation import (
    evaluate as evaluate_parameter_f021,
)
from symbolic_eval.f096.object_creation import (
    evaluate as evaluate_parameter_f096,
)
from symbolic_eval.f134.object_creation import (
    evaluate as evaluate_parameter_f134,
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
    FindingEnum.F001: evaluate_parameter_f001,
    FindingEnum.F004: evaluate_parameter_f004,
    FindingEnum.F015: evaluate_parameter_f015,
    FindingEnum.F016: evaluate_parameter_f016,
    FindingEnum.F021: evaluate_parameter_f021,
    FindingEnum.F096: evaluate_parameter_f096,
    FindingEnum.F134: evaluate_parameter_f134,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    if al_id := args.graph.nodes[args.n_id].get("arguments_id"):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(al_id)).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
