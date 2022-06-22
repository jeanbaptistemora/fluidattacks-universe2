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
    var_type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    var_decl_id = match_ast_d(args.ast_graph, args.n_id, "variable_declarator")

    if not var_decl_id:
        raise MissingCaseHandling(f"Bad variable declarator in {args.n_id}")

    match = match_ast(args.ast_graph, var_decl_id, "identifier")
    value_id = match.get("__1__")

    if not value_id:
        raise MissingCaseHandling(f"Bad variable declarator in {args.n_id}")

    var_type = node_to_str(args.ast_graph, var_type_id)
    var = node_to_str(args.ast_graph, str(match["identifier"]))

    return build_variable_declaration_node(args, var, var_type, value_id)
