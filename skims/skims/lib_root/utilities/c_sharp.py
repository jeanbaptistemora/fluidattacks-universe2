from model import (
    graph_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
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


def get_variable_attribute(
    graph: graph_model.GraphShard, name_var: str, attribute: str
) -> str:
    for member in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(
            label_type="identifier", label_text=name_var
        ),
    ):
        pred = g.pred(graph, member)[0]
        if graph.nodes[pred].get("label_type") == "variable_declarator":
            declaration_node = g.match_ast(graph, pred, "__0__")["__1__"]
            value_node = g.match_ast(graph, declaration_node, "__0__")["__1__"]
            if (
                graph.nodes[value_node].get("label_type")
                == "invocation_expression"
            ):
                if attribute == "label_text":
                    return build_member_access_expression_key(
                        graph, g.match_ast(graph, value_node, "__0__")["__0__"]
                    )
                if attribute == "label_type":
                    return graph.nodes[value_node].get("label_type")
            return graph.nodes[value_node].get(attribute)
    return ""


def yield_member_access(
    graph_db: GraphDB, members: Set[str]
) -> GraphShardNodes:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.CSHARP,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="member_access_expression"),
        ):
            match = g.match_ast(shard.graph, member, "__0__")
            if shard.graph.nodes[match["__0__"]].get("label_text") in members:
                yield shard, member


def yield_object_creation(
    graph_db: GraphDB, members: Set[str]
) -> GraphShardNodes:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.CSHARP,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(
                label_type="object_creation_expression"
            ),
        ):
            match = g.match_ast(shard.graph, member, "identifier")
            if (identifier := match["identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member


def yield_invocation_expression(
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
