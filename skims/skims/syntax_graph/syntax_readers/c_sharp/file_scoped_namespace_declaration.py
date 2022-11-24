from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.file_scoped_namespace_declaration import (
    build_file_namespace_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    valid_types = {
        "class_declaration",
        "delegate_declaration",
        "enum_declaration",
        "extern_alias_directive",
        "interface_declaration",
        "record_declaration",
        "record_struct_declaration",
        "struct_declaration",
        "using_directive",
    }

    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    name = node_to_str(args.ast_graph, name_id)
    childs_id = adj_ast(args.ast_graph, args.n_id)

    return build_file_namespace_node(
        args,
        name,
        c_ids=(
            c_id
            for c_id in childs_id
            if graph.nodes[c_id]["label_type"] in valid_types
        ),
    )
