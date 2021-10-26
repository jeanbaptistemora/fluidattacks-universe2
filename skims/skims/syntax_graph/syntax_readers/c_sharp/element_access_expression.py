from syntax_graph.syntax_nodes.element_access import (
    build_element_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> str:
    expression_id = args.ast_graph.nodes[args.n_id]["label_field_expression"]
    arguments_id = args.ast_graph.nodes[args.n_id]["label_field_subscript"]

    return build_element_access_node(args, expression_id, arguments_id)
