from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.new_expression import (
    build_new_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    constructor_id = args.ast_graph.nodes[args.n_id]["label_field_constructor"]
    arguments_id = args.ast_graph.nodes[args.n_id].get("label_field_arguments")

    return build_new_expression_node(args, constructor_id, arguments_id)
