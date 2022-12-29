from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    body_id = graph.nodes[args.n_id]["label_field_body"]
    if graph.nodes[body_id]["label_type"] == "expression_statement":
        body_id = adj_ast(graph, body_id)[0]

    condition_node = graph.nodes[args.n_id]["label_field_condition"]

    return build_do_statement_node(args, body_id, condition_node)
