from model import (
    graph_model,
)
from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    NId,
)
from typing import (
    Any,
    Iterator,
    Optional,
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
    node_var: str = ""
    for syntax_steps in shard.syntax.values():
        for syntax_step in syntax_steps:
            if (
                isinstance(syntax_step, graph_model.SyntaxStepDeclaration)
                and syntax_step.var == name_var
                and shard.graph.nodes[syntax_step.meta.n_id].get("label_type")
                != "parameter"
            ):
                node_var = str(
                    g.match_ast(
                        shard.graph,
                        syntax_step.meta.n_id,
                        "equals_value_clause",
                        depth=2,
                    )["equals_value_clause"]
                )
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
        for member in yield_shard_member_access(shard, members):
            yield shard, member


def yield_shard_member_access(
    shard: GraphShard, members: Set[str]
) -> Iterator[NId]:
    for member in g.filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=g.pred_has_labels(label_type="member_access_expression"),
    ):
        match = g.match_ast(shard.graph, member, "__0__")
        if shard.graph.nodes[match["__0__"]].get("label_text") in members:
            yield member


def yield_object_creation(
    graph_db: GraphDB, members: Set[str]
) -> GraphShardNodes:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.CSHARP,
    ):
        for member in yield_shard_object_creation(shard, members):
            yield shard, member


def yield_shard_object_creation(
    shard: GraphShard, members: Set[str]
) -> Iterator[NId]:
    for member in g.filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=g.pred_has_labels(label_type="object_creation_expression"),
    ):
        if qualified := g.match_ast(shard.graph, member, "qualified_name").get(
            "qualified_name"
        ):
            member = qualified
        match = g.match_ast(shard.graph, member, "identifier")
        if (
            match.get("identifier")
            and (identifier := match["identifier"])
            and shard.graph.nodes[identifier]["label_text"] in members
        ):
            yield member


def yield_invocation_expression(
    graph_db: graph_model.GraphDB,
) -> Iterator[Tuple[graph_model.GraphShard, NId, str]]:
    for shard in graph_db.shards_by_language(
        graph_model.GraphShardMetadataLanguage.CSHARP,
    ):
        for member, method in yield_shard_invocation_expression(shard):
            yield shard, member, method


def yield_shard_invocation_expression(
    shard: GraphShard,
) -> Iterator[Tuple[NId, str]]:
    for invoc_id in g.filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=g.pred_has_labels(label_type="invocation_expression"),
    ):
        method_id = shard.graph.nodes[invoc_id]["label_field_function"]
        yield invoc_id, node_to_str(shard.graph, method_id)


def get_object_argument_list(
    shard: graph_model.GraphShard, obj_id: str
) -> str:
    n_args = g.get_ast_childs(
        shard.graph,
        g.get_ast_childs(shard.graph, obj_id, "argument_list")[0],
        "argument",
    )[0]
    return node_to_str(shard.graph, n_args)


def get_first_member(
    shard: graph_model.GraphShard, n_id: str
) -> Optional[str]:
    member: Any = g.match_ast(shard.graph, n_id, "member_access_expression")
    while member.get("member_access_expression"):
        member = member.get("member_access_expression")
        member = g.match_ast(shard.graph, member, "member_access_expression")
    return member["__0__"]


def get_var_node_from_obj(
    shard: graph_model.GraphShard, n_id: str
) -> Optional[str]:
    depth = (
        3 if shard.graph.nodes[n_id]["label_type"] == "qualified_name" else 2
    )
    if (
        (preds := g.pred_ast(shard.graph, n_id, depth))
        and len(preds) > 1
        and shard.graph.nodes[preds[-1]]["label_type"] == "variable_declarator"
    ):
        return g.match_ast_d(shard.graph, preds[-1], "identifier")
    return None
