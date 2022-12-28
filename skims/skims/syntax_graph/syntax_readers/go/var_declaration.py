from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    declarator_id = match_ast_d(args.ast_graph, args.n_id, "var_spec")

    var_id = args.ast_graph.nodes[declarator_id]["label_field_name"]
    var_name = node_to_str(args.ast_graph, var_id)

    type_id = args.ast_graph.nodes[declarator_id].get("label_field_type")
    type_name = node_to_str(args.ast_graph, type_id)

    value_id = args.ast_graph.nodes[declarator_id].get("label_field_value")

    return build_variable_declaration_node(args, var_name, type_name, value_id)
