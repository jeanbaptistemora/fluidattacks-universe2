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
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    declarator_id = match_ast_d(
        args.ast_graph, args.n_id, "variable_declarator"
    )
    if not declarator_id:
        raise MissingCaseHandling(f"Bad variable declaration in {args.n_id}")

    var_id = args.ast_graph.nodes[declarator_id]["label_field_name"]
    var_name = node_to_str(args.ast_graph, var_id)

    value_id = args.ast_graph.nodes[declarator_id].get("label_field_value")

    return build_variable_declaration_node(args, var_name, None, value_id)
