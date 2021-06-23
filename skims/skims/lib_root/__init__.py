from model import (
    graph_model,
)
from typing import (
    Iterable,
    Tuple,
)
from utils import (
    graph as g,
)


def yield_java_method_invocation(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_langauge(
        graph_model.GraphShardMetadataLanguage.JAVA,
    ):
        for method_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="method_invocation"),
        ):
            match = g.match_ast_group(
                shard.graph,
                method_id,
                "argument_list",
                "identifier",
                "field_access",
            )
            method_name = g.concatenate_label_text(
                shard.graph, match["identifier"], separator="."
            )
            if match["field_access"]:
                base_name = shard.graph.nodes[match["field_access"][0]][
                    "label_text"
                ]
                method_name = base_name + "." + method_name
            yield shard, method_id, method_name


def yield_java_object_creation(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_langauge(
        graph_model.GraphShardMetadataLanguage.JAVA,
    ):
        for object_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(
                label_type="object_creation_expression"
            ),
        ):
            match = g.match_ast(
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
