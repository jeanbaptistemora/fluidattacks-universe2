from model.graph_model import (
    Graph,
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    NId,
)
from typing import (
    Iterable,
    Optional,
    Tuple,
)
from utils.graph import (
    concatenate_label_text,
    match_ast,
    match_ast_group,
    matching_nodes,
)


def yield_object_creation(
    graph_db: GraphDB,
) -> Iterable[Tuple[GraphShard, str, str]]:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.JAVA,
    ):
        for object_id in matching_nodes(
            shard.graph, label_type="object_creation_expression"
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
        for method_id in matching_nodes(
            shard.graph, label_type="method_invocation"
        ):
            match = match_ast_group(
                shard.graph,
                method_id,
                "argument_list",
                "identifier",
                "field_access",
            )
            method_name = concatenate_label_text(
                shard.graph, tuple(match["identifier"]), separator="."
            )
            if match["field_access"]:
                base_name = shard.graph.nodes[match["field_access"][0]][
                    "label_text"
                ]
                method_name = base_name + "." + method_name
            yield shard, method_id, method_name


def concatenate_name(
    graph: Graph, n_id: NId, name: Optional[str] = None
) -> str:
    if name:
        prev_str = "." + name
    else:
        prev_str = ""

    node_type = graph.nodes[n_id]["label_type"]
    if node_type == "MethodInvocation":
        expr = graph.nodes[n_id]["expression"]
        if graph.nodes[n_id].get("object_id") and (
            next_node := match_ast(graph, n_id)["__0__"]
        ):
            expr = concatenate_name(graph, next_node, expr)
    elif node_type == "SymbolLookup":
        expr = graph.nodes[n_id]["symbol"]
    elif node_type == "FieldAccess":
        expr = graph.nodes[n_id]["field_text"]
    else:
        expr = ""
    return expr + prev_str


def yield_method_invocation_syntax_graph(
    graph: Graph,
) -> Iterable[Tuple[str, str]]:
    for n_id in matching_nodes(graph, label_type="MethodInvocation"):
        method_name = concatenate_name(graph, n_id)
        yield n_id, method_name
