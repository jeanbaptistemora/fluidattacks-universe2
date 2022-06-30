from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.interface_declaration import (
    build_interface_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    name = node_to_str(args.ast_graph, name_id)
    body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
    return build_interface_declaration_node(args, name, body_id, None)
