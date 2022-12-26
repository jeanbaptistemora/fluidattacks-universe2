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
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    var_name = "Unnamed"
    var_type = "Local"

    var_dec = match_ast_d(graph, args.n_id, "variable_declaration")
    var_type_id = match_ast_d(graph, args.n_id, "modifiers")

    if var_dec:
        var_name = node_to_str(graph, var_dec)
    if var_type_id:
        var_type = node_to_str(graph, var_type_id)

    value_id = adj_ast(graph, args.n_id)[-1]
    val_id_type = graph.nodes[value_id]["label_type"]
    if val_id_type == "variable_declaration":
        value_id = None
    elif val_id_type == "property_delegate":
        value_id = match_ast_d(graph, value_id, "call_expression")

    return build_variable_declaration_node(args, var_name, var_type, value_id)
