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
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]

    name_id = n_attrs.get("label_field_identifier")
    name = node_to_str(graph, name_id) if name_id else "AnonymousMethod"

    block_id = n_attrs.get("label_field_function_body")
    parameters_list = match_ast_group_d(graph, args.n_id, "parameter")
    children_nid = {
        "parameters_id": parameters_list,
    }

    return build_method_declaration_node(args, name, block_id, children_nid)
