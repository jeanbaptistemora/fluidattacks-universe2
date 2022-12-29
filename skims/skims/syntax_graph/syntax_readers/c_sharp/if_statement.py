from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    condition_id = graph.nodes[args.n_id]["label_field_condition"]

    true_id = graph.nodes[args.n_id]["label_field_consequence"]
    if graph.nodes[true_id]["label_type"] == "expression_statement":
        true_id = adj_ast(graph, true_id)[0]

    false_id = graph.nodes[args.n_id].get("label_field_alternative")
    if (
        false_id
        and graph.nodes[false_id]["label_type"] == "expression_statement"
    ):
        false_id = adj_ast(graph, false_id)[0]

    return build_if_node(args, condition_id, true_id, false_id)
