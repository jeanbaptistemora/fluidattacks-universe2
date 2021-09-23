from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from typing import (
    Set,
)
from utils.graph import (
    filter_nodes,
    match_ast,
    pred_has_labels,
)


def yield_object_creation(
    graph_db: GraphDB, members: Set[str]
) -> GraphShardNodes:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.GO,
    ):
        for member in filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=pred_has_labels(label_type="selector_expression"),
        ):
            match = match_ast(shard.graph, member, "identifier")
            if (identifier := match["identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member


def yield_member_access(
    graph_db: GraphDB, members: Set[str]
) -> GraphShardNodes:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.GO,
    ):
        for member in filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=pred_has_labels(label_type="selector_expression"),
        ):
            match = match_ast(shard.graph, member, "field_identifier")
            if (identifier := match["field_identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member
