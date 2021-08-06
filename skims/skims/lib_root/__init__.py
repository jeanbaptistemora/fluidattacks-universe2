from model import (
    graph_model,
)
from typing import (
    Iterable,
    Set,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_member_access_expression_key,
)


def get_composite_name_kotlin(
    graph: graph_model.Graph, n_id: graph_model.NId
) -> str:
    # Function to build the name of a function/argument that has multiple
    # levels, e.g. ConnectionSpec.Builder.tlsVersions
    # For it to work, n_id must have children nodes of the type
    # `navigation_expression`.
    # n_id itself should not be a `navigation_expression` node, use its parent
    composite_name: str = ""
    match = g.match_ast(
        graph,
        n_id,
        "navigation_expression",
        "simple_identifier",
    )
    while nav_expr := match["navigation_expression"]:
        match = g.match_ast(
            graph,
            nav_expr,
            "call_expression",
            "navigation_expression",
            "navigation_suffix",
            "simple_identifier",
        )
        composite_name = (
            g.concatenate_label_text(
                graph,
                g.adj_ast(graph, match["navigation_suffix"]),
            )
            + composite_name
        )
        if call_expr := match["call_expression"]:
            match = g.match_ast(
                graph,
                call_expr,
                "navigation_expression",
                "simple_identifier",
            )
    composite_name = (
        graph.nodes[match["simple_identifier"]]["label_text"] + composite_name
    )
    return composite_name


def yield_java_method_invocation(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
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
    for shard in graph_db.shards_by_language(
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


def yield_kotlin_method_invocation(
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
            method_name = get_composite_name_kotlin(shard.graph, method_id)
            yield shard, method_id, method_name


def yield_c_sharp_invocation_expression(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
        graph_model.GraphShardMetadataLanguage.CSHARP,
    ):
        for method_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="invocation_expression"),
        ):
            method_name = build_member_access_expression_key(
                shard.graph,
                method_id,
            )

            yield shard, method_id, method_name


def yield_go_object_creation(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_language(
        graph_model.GraphShardMetadataLanguage.GO,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="selector_expression"),
        ):
            match = g.match_ast(shard.graph, member, "identifier")
            if (identifier := match["identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member


def yield_go_member_access(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_language(
        graph_model.GraphShardMetadataLanguage.GO,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="selector_expression"),
        ):
            match = g.match_ast(shard.graph, member, "field_identifier")
            if (identifier := match["field_identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member
