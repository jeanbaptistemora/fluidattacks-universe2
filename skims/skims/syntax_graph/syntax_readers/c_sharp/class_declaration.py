from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
    match_ast_group,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    class_node = args.ast_graph.nodes[args.n_id]
    declaration_n_id = match_ast_d(args.ast_graph, args.n_id, "identifier")
    declaration_node = args.ast_graph.nodes[declaration_n_id]
    declaration_line = declaration_node["label_l"]
    args.ast_graph.nodes[args.n_id]["label_l"] = declaration_line
    name_id = class_node["label_field_name"]
    block_id = class_node["label_field_body"]
    name = node_to_str(args.ast_graph, name_id)
    match_childs = match_ast_group(args.ast_graph, args.n_id, "attribute_list")
    attributes = match_childs.get("attribute_list")
    return build_class_node(args, name, block_id, attributes)
