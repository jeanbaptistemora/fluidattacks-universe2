from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.f008.cases.parameter.c_sharp import (
    evaluate as c_sharp_evaluate,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)

LANGUAGE_EVALUATORS: Dict[GraphLanguage, Evaluator] = {
    GraphLanguage.CSHARP: c_sharp_evaluate,
}


def evaluate(args: SymbolicEvalArgs) -> bool:
    if language_evaluator := LANGUAGE_EVALUATORS.get(args.language):
        return language_evaluator(args)
    return args.graph.nodes[args.n_id]["danger"]
