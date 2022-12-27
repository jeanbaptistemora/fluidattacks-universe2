from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
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
    types = {
        "array_type",
        "channel_type",
        "function_type",
        "generic_type",
        "interface_type",
        "map_type",
        "pointer_type",
        "qualified_type",
        "slice_type",
        "struct_type",
        "type_identifier",
    }
    spec_id = None
    var_name = None
    var_type = None
    for c_id in adj_ast(graph, args.n_id):
        if graph.nodes[c_id]["label_type"] == "type_spec":
            spec_id = c_id
            id_name = graph.nodes[c_id]["label_field_name"]
            var_name = node_to_str(graph, id_name)
    for t_id in adj_ast(graph, str(spec_id)):
        if graph.nodes[t_id]["label_type"] in types:
            var_type = node_to_str(graph, t_id)

    return build_variable_declaration_node(args, var_name, var_type, None)
