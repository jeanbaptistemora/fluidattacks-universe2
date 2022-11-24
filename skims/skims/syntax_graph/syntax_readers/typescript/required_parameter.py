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
    n_attrs = args.ast_graph.nodes[args.n_id]

    pattern_id = n_attrs.get("label_field_pattern") or n_attrs.get(
        "label_field_name"
    )
    var_name = node_to_str(args.ast_graph, pattern_id) if pattern_id else None

    type_id = n_attrs.get("label_field_type")
    var_type = None
    if type_id:
        var_type = node_to_str(args.ast_graph, type_id).replace(":", "")

    def_value = n_attrs.get("label_field_value")

    return build_parameter_node(args, var_name, var_type, def_value)
