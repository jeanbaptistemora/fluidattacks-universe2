from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f001.parameter import (
    evaluate as evaluate_parameter_f001,
)
from symbolic_eval.f004.parameter import (
    evaluate as evaluate_parameter_f004,
)
from symbolic_eval.f008.parameter import (
    evaluate as evaluate_parameter_f008,
)
from symbolic_eval.f015.parameter import (
    evaluate as evaluate_parameter_f015,
)
from symbolic_eval.f021.parameter import (
    evaluate as evaluate_parameter_f021,
)
from symbolic_eval.f063.parameter import (
    evaluate as evaluate_parameter_f063,
)
from symbolic_eval.f089.parameter import (
    evaluate as evaluate_parameter_f089,
)
from symbolic_eval.f091.parameter import (
    evaluate as evaluate_parameter_f091,
)
from symbolic_eval.f096.parameter import (
    evaluate as evaluate_parameter_f096,
)
from symbolic_eval.f098.parameter import (
    evaluate as evaluate_parameter_f098,
)
from symbolic_eval.f100.parameter import (
    evaluate as evaluate_parameter_f100,
)
from symbolic_eval.f107.parameter import (
    evaluate as evaluate_parameter_f107,
)
from symbolic_eval.f112.parameter import (
    evaluate as evaluate_parameter_f112,
)
from symbolic_eval.f211.parameter import (
    evaluate as evaluate_parameter_f211,
)
from symbolic_eval.f413.parameter import (
    evaluate as evaluate_parameter_f413,
)
from symbolic_eval.f416.parameter import (
    evaluate as evaluate_parameter_f416,
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
    FindingEnum.F008: evaluate_parameter_f008,
    FindingEnum.F015: evaluate_parameter_f015,
    FindingEnum.F021: evaluate_parameter_f021,
    FindingEnum.F063: evaluate_parameter_f063,
    FindingEnum.F089: evaluate_parameter_f089,
    FindingEnum.F091: evaluate_parameter_f091,
    FindingEnum.F096: evaluate_parameter_f096,
    FindingEnum.F098: evaluate_parameter_f098,
    FindingEnum.F100: evaluate_parameter_f100,
    FindingEnum.F107: evaluate_parameter_f107,
    FindingEnum.F112: evaluate_parameter_f112,
    FindingEnum.F211: evaluate_parameter_f211,
    FindingEnum.F413: evaluate_parameter_f413,
    FindingEnum.F416: evaluate_parameter_f416,
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
