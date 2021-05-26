# Standard librari
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional,
)

# Third libraries
from mypy_extensions import (
    DefaultArg,
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
            DefaultArg(Any, None),
        ],
        None,
    ]
    eval_constructor: Callable[
        [
            Any,
            graph_model.NId,
            graph_model.SyntaxSteps,
            graph_model.GraphShard,
            str,
        ],
        graph_model.CurrentInstance,
    ]
    finding: core_model.FindingEnum
    graph_db: graph_model.GraphDB
    shard: graph_model.GraphShard
    n_id_next: graph_model.NId
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps
    current_instance: Optional[graph_model.CurrentInstance] = None


Evaluator = Callable[[EvaluatorArgs], None]

# Java


class LookedUpJavaClass(NamedTuple):
    metadata: graph_model.GraphShardMetadataClass
    shard_path: str


class LookedUpJavaMethod(NamedTuple):
    metadata: graph_model.GraphShardMetadataClassMethod
    shard_path: str


class LookedUpJavaClassField(NamedTuple):
    metadata: graph_model.GraphShardMetadataClassField
    shard_path: str


class JavaClassInstance(NamedTuple):
    fields: Dict[str, Optional[graph_model.SyntaxStep]]
    class_name: Optional[str] = None
