from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.field_declaration import (
    build_field_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    vars_list = match_ast_group_d(
        args.ast_graph, args.n_id, "variable_declarator"
    )
    field_type = node_to_str(args.ast_graph, type_id)
    return build_field_declaration_node(args, vars_list, field_type)
