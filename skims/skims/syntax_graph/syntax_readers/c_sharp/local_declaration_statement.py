from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    decl_id = match_ast_d(args.ast_graph, args.n_id, "variable_declaration")
    if not decl_id:
        raise MissingCaseHandling(f"Bad local declaration in {args.n_id}")

    var_type_id = args.ast_graph.nodes[decl_id]["label_field_type"]
    var_type = node_to_str(args.ast_graph, var_type_id)
    value_id = None

    var_decl_id = match_ast_d(args.ast_graph, decl_id, "variable_declarator")
    if not var_decl_id:
        raise MissingCaseHandling(f"Bad local declaration in {args.n_id}")

    identifier_id = match_ast_d(args.ast_graph, var_decl_id, "identifier")
    equals_id = match_ast_d(args.ast_graph, var_decl_id, "equals_value_clause")

    if not identifier_id:
        raise MissingCaseHandling(f"Bad local declaration in {args.n_id}")

    var = node_to_str(args.ast_graph, identifier_id)

    if equals_id:
        match_eq = match_ast(args.ast_graph, equals_id, "=")
        if len(match_eq) != 2 or not match_eq.get("="):
            raise MissingCaseHandling(f"Bad equal value in {args.n_id}")
        value_id = match_eq["__0__"]

    return build_variable_declaration_node(args, var, var_type, value_id)
