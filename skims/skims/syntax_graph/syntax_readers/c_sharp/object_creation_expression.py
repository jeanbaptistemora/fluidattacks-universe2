from syntax_graph.syntax_nodes.object_creation import (
    build_object_creation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> str:
    l_arg = "label_field_arguments"
    l_type = "label_field_type"

    node_attr = args.ast_graph.nodes[args.n_id]
    type_id = node_attr[l_type]
    arguments_id = node_attr.get(l_arg)
    name = node_to_str(args.ast_graph, type_id)

    return build_object_creation_node(args, name, arguments_id)
