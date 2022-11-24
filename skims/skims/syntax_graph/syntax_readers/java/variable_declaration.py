from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    var_type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    var_type = node_to_str(args.ast_graph, var_type_id)

    declarator_id = args.ast_graph.nodes[args.n_id]["label_field_declarator"]

    var_id = args.ast_graph.nodes[declarator_id]["label_field_name"]
    var_name = node_to_str(args.ast_graph, var_id)

    value_id = args.ast_graph.nodes[declarator_id].get("label_field_value")

    return build_variable_declaration_node(args, var_name, var_type, value_id)
