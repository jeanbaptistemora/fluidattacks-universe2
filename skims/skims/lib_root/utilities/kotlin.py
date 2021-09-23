from model import (
    graph_model,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
)
from typing import (
    Iterable,
    Tuple,
)
from utils import (
    graph as g,
)


def yield_method_invocation(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
        graph_model.GraphShardMetadataLanguage.KOTLIN,
    ):
        for method_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="call_expression"),
        ):
            method_name = get_composite_name(shard.graph, method_id)
            yield shard, method_id, method_name
