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
    var_dec = match_ast_d(args.ast_graph, args.n_id, "variable_declaration")
    var_type_id = match_ast_d(args.ast_graph, args.n_id, "modifiers")
    if not (var_dec and var_type_id):
        var_name = "Unnamed"
        var_type = "local"
    else:
        var_type = node_to_str(args.ast_graph, var_type_id)
        var_name = node_to_str(args.ast_graph, var_dec)

    value_id = adj_ast(args.ast_graph, args.n_id)[-1]

    if args.ast_graph.nodes[value_id]["label_type"] == "variable_declaration":
        value_id = None

    return build_variable_declaration_node(args, var_name, var_type, value_id)
