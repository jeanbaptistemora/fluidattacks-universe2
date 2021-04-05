# Standard librari
from typing import (
    Any,
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
    eval_method: Callable[
        [
            Any,
            graph_model.NId,
            graph_model.SyntaxSteps,
            graph_model.GraphShard,
        ],
        None,
    ]
    finding: core_model.FindingEnum
    graph_db: graph_model.GraphDB
    shard: graph_model.GraphShard
    n_id_next: graph_model.NId
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]


# Java


class LookedUpJavaClass(NamedTuple):
    metadata: graph_model.GraphShardMetadataJavaClass
    shard_path: str


class LookedUpJavaMethod(NamedTuple):
    metadata: graph_model.GraphShardMetadataJavaClassMethod
    shard_path: graph_model.GraphShard
