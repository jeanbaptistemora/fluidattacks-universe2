from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.element_access import (
    build_element_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    arguments_id = n_attrs["label_field_subscript"]
    expr_id = n_attrs["label_field_value"]
    return build_element_access_node(args, expr_id, arguments_id)
