from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> str:
    var_type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    var_decl = match_ast_d(args.ast_graph, args.n_id, "variable_declarator")

    equals_clause = "equals_value_clause"
    match = match_ast(args.ast_graph, var_decl, "identifier", equals_clause)

    match_eq = match_ast(args.ast_graph, match["equals_value_clause"], "=")
    value_id = match_eq["__0__"]

    var = node_to_str(args.ast_graph, match["identifier"])
    var_type = node_to_str(args.ast_graph, var_type_id)

    return build_variable_declaration_node(args, var, var_type, value_id)
