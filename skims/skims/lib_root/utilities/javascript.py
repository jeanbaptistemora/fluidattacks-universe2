from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    SyntaxStepMethodInvocation,
    SyntaxSteps,
)
from typing import (
    Iterable,
    Tuple,
)


def yield_method_invocation(
    graph_db: GraphDB,
) -> Iterable[
    Tuple[
        GraphShard,
        SyntaxSteps,
        SyntaxStepMethodInvocation,
        int,
    ]
]:
    for shard in [
        *graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ),
        *graph_db.shards_by_language(
            GraphShardMetadataLanguage.TSX,
        ),
    ]:
        for syntax_steps in shard.syntax.values():
            for index, invocation_step in enumerate(syntax_steps):
                if invocation_step.type != "SyntaxStepMethodInvocation":
                    continue
                yield shard, syntax_steps, invocation_step, index
