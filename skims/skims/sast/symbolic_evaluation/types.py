# Standard librari
from typing import (
    Callable,
    NamedTuple,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)


class StopEvaluation(Exception):
    pass


class ImpossiblePath(StopEvaluation):
    pass


class EvaluatorArgs(NamedTuple):
    dependencies: graph_model.SyntaxSteps
    finding: core_model.FindingEnum
    graph_db: graph_model.GraphDB
    shard: graph_model.GraphShard
    n_id_next: graph_model.NId
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]
