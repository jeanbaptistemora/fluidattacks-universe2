from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> str:
    method = args.ast_graph.nodes[args.n_id]
    name_id = method["label_field_name"]
    parameters_id = method["label_field_parameters"]
    block_id = method["label_field_body"]
    name = node_to_str(args.ast_graph, name_id)
    return build_method_declaration_node(args, name, block_id, parameters_id)
