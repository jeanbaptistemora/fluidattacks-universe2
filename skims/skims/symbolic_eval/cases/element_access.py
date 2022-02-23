from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f021.element_access import (
    evaluate as evaluate_element_access_f021,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F021: evaluate_element_access_f021,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    acces_attr = args.graph.nodes[args.n_id]
    d_arguments = args.generic(args.fork_n_id(acces_attr["arguments_id"]))
    d_expression = args.generic(args.fork_n_id(acces_attr["expression_id"]))

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
