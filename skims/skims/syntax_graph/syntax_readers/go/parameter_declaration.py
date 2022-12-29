from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    var_id = args.ast_graph.nodes[args.n_id].get("label_field_name")
    if var_id:
        var_name = node_to_str(args.ast_graph, var_id)
    type_id = args.ast_graph.nodes[args.n_id]["label_field_type"]
    var_type = node_to_str(args.ast_graph, type_id)

    return build_parameter_node(args, var_name, var_type, None)
