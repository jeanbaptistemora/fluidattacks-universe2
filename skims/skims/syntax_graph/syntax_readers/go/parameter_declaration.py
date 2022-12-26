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

    var_id = args.ast_graph.nodes[args.n_id].get("label_field_name")
    if var_id:
        var_name = node_to_str(args.ast_graph, var_id)

    type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    type_var = node_to_str(args.ast_graph, type_id)

    return build_variable_declaration_node(args, var_name, type_var, None)
