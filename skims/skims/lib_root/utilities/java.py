from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
)
from typing import (
    Iterable,
    Tuple,
)
from utils.graph import (
    concatenate_label_text,
    filter_nodes,
    match_ast,
    match_ast_group,
    pred_has_labels,
)


def yield_object_creation(
    graph_db: GraphDB,
) -> Iterable[Tuple[GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.JAVA,
    ):
        for object_id in filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=pred_has_labels(label_type="object_creation_expression"),
        ):
            match = match_ast(
                shard.graph,
                object_id,
                "new",
                "argument_list",
                "type_identifier",
                "scoped_type_identifier",
            )
            if scoped_type := match["scoped_type_identifier"]:
                type_name = shard.graph.nodes[scoped_type]["label_text"]
                yield shard, object_id, type_name
            elif type_identifier := match["type_identifier"]:
                type_name = shard.graph.nodes[type_identifier]["label_text"]
                yield shard, object_id, type_name


def yield_method_invocation(
    graph_db: GraphDB,
) -> Iterable[Tuple[GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.JAVA,
    ):
        for method_id in filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=pred_has_labels(label_type="method_invocation"),
        ):
            match = match_ast_group(
                shard.graph,
                method_id,
                "argument_list",
                "identifier",
                "field_access",
            )
            method_name = concatenate_label_text(
                shard.graph, match["identifier"], separator="."
            )
            if match["field_access"]:
                base_name = shard.graph.nodes[match["field_access"][0]][
                    "label_text"
                ]
                method_name = base_name + "." + method_name
            yield shard, method_id, method_name
