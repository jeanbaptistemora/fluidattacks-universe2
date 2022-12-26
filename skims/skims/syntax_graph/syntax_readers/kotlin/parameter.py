from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    var_name = "UnnamedParam"
    var_type = None
    val_id = None
    if n_attrs.get("label_field_expression"):
        val_id = n_attrs["label_field_expression"]
        var_name = node_to_str(graph, val_id)
        var_type = None
    elif n_attrs.get("label_field_identifier"):
        val_id = n_attrs["label_field_identifier"]
        var_type_id = match_ast_d(graph, args.n_id, "user_type")
        var_type = node_to_str(graph, var_type_id) if var_type_id else None

    return build_parameter_node(args, var_name, var_type, val_id)
