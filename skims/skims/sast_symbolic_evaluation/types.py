from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from mypy_extensions import (
    DefaultArg,
)
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional,
)


class StopEvaluation(Exception):
    @classmethod
    def from_args(cls, args: EvaluatorArgs) -> StopEvaluation:
        path: str = args.shard.path
        n_id: graph_model.NId = args.syntax_step.meta.n_id
        return StopEvaluation(f"Incomplete Syntax Reader, {path} @ {n_id}")


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
    shard_db: ShardDb
    graph_db: graph_model.GraphDB
    shard: graph_model.GraphShard
    n_id_next: graph_model.NId
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps
    current_instance: Optional[graph_model.CurrentInstance] = None


Evaluator = Callable[[EvaluatorArgs], None]

# Go


@dataclass
class GoParsedFloat:
    is_inf: bool = True
    is_nan: bool = True
    method_n_id: str = ""
    shard_idx: Optional[int] = None


# Java


class LookedUpClass(NamedTuple):
    metadata: graph_model.GraphShardMetadataClass
    shard_path: str


class LookedUpMethod(NamedTuple):
    metadata: graph_model.GraphShardMetadataClassMethod
    shard_path: str


class LookedUpClassField(NamedTuple):
    metadata: graph_model.GraphShardMetadataClassField
    shard_path: str


class JavaClassInstance(NamedTuple):
    fields: Dict[str, Optional[graph_model.SyntaxStep]]
    class_name: Optional[str] = None
