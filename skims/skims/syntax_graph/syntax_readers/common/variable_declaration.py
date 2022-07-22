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
    var_type = None

    if var_type_id := args.ast_graph.nodes[args.n_id].get("label_field_type"):
        var_type = node_to_str(args.ast_graph, var_type_id)

    declarator_id = match_ast_d(
        args.ast_graph, args.n_id, "variable_declarator"
    )

    if not declarator_id:
        raise MissingCaseHandling(f"Bad variable declarator in {args.n_id}")

    return build_variable_declaration_node(
        args, None, var_type, None, declarator_id
    )
