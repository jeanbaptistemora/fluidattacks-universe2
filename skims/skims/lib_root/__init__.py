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
from utils.graph.transformation import (
    build_member_access_expression_key,
)


def csharp_get_variable_attribute(
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
