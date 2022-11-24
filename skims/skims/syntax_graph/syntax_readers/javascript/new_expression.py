from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.object_creation import (
    build_object_creation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    constructor_id = args.ast_graph.nodes[args.n_id]["label_field_constructor"]
    name = node_to_str(args.ast_graph, constructor_id)
    arguments_id = args.ast_graph.nodes[args.n_id].get("label_field_arguments")
    return build_object_creation_node(args, name, arguments_id, None)
