from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    name = "CompanionObject"
    name_id = match_ast_d(graph, args.n_id, "type_identifier")
    if name_id:
        name = node_to_str(graph, name_id)

    block_id = match_ast_d(graph, args.n_id, "class_body")

    modifiers = match_ast_group_d(graph, args.n_id, "modifiers")
    children_nid = {
        "modifiers_id": modifiers,
    }

    return build_method_declaration_node(args, name, block_id, children_nid)
