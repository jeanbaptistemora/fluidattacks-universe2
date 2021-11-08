from model.core_model import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    m_attr = args.graph.nodes[args.n_id]
    m_attr["danger"] = args.generic(args.fork_n_id(m_attr["parameters_id"]))

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        m_attr["danger"] = finding_evaluator(args)

    return m_attr["danger"]
