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
from utils.graph.text_nodes import (
    node_to_str,
)


def get_variable_attribute(
    shard: graph_model.GraphShard, name_var: str, attribute: str
) -> str:
    node_var = ""
    for syntax_steps in shard.syntax.values():
        for syntax_step in syntax_steps:
            if (
                isinstance(syntax_step, graph_model.SyntaxStepDeclaration)
                and syntax_step.var == name_var
                and shard.graph.nodes[syntax_step.meta.n_id].get("label_type")
                != "parameter"
            ):
                node_var = g.match_ast(
                    shard.graph,
                    syntax_step.meta.n_id,
                    "equals_value_clause",
                    depth=2,
                )["equals_value_clause"]
                node_index = 1
            elif (
                isinstance(syntax_step, graph_model.SyntaxStepAssignment)
                and syntax_step.var == name_var
            ):
                node_var = syntax_step.meta.n_id
                node_index = 2
    if (
        len(node_var) > 0
        and g.adj_ast(shard.graph, node_var)
        and len(var_value := g.adj_ast(shard.graph, node_var)) > node_index
    ):
        if attribute == "text":
            return node_to_str(shard.graph, var_value[node_index])
        if attribute == "type":
            return shard.graph.nodes[var_value[node_index]].get("label_type")
    return node_var


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
        for invoc_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="invocation_expression"),
        ):
            method_id = shard.graph.nodes[invoc_id]["label_field_function"]
            yield shard, invoc_id, node_to_str(shard.graph, method_id)
