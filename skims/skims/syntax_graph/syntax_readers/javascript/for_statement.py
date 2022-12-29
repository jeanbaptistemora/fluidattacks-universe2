from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_statement import (
    build_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]
    if graph.nodes[body_id]["label_type"] == "expression_statement":
        body_id = match_ast(graph, body_id)["__0__"]
    if graph.nodes[body_id]["label_type"] == "parenthesized_expression":
        body_id = match_ast(graph, body_id)["__1__"]

    initializer_id = n_attrs["label_field_initializer"]
    if graph.nodes[initializer_id]["label_type"] == "expression_statement":
        initializer_id = match_ast(graph, initializer_id)["__0__"]

    condition_id = n_attrs["label_field_condition"]
    increment_id = n_attrs.get("label_field_increment")

    return build_for_statement_node(
        args, initializer_id, condition_id, increment_id, body_id
    )
