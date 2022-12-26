from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]

    condition_id = n_attrs.get("label_field_condition_expression")
    true_id = n_attrs.get("label_field_body")
    if not (condition_id and true_id):
        raise MissingCaseHandling(f"Bad if expression handling in {args.n_id}")

    if graph.nodes[condition_id]["label_type"] == "parenthesized_expression":
        condition_id = match_ast(graph, condition_id).get("__1__")

    false_id = n_attrs.get("label_field_else_body")
    return build_if_node(args, condition_id, true_id, false_id)
