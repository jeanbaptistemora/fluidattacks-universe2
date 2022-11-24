from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    body_id = graph.nodes[args.n_id]["label_field_body"]
    condition_node = graph.nodes[args.n_id]["label_field_condition"]

    return build_do_statement_node(args, body_id, condition_node)
