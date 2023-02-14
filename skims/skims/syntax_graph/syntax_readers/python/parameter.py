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
    var_type = None
    var_name = "UnnamedVar"

    type_id = n_attrs.get("label_field_type")
    if type_id:
        var_type = node_to_str(graph, type_id)
    identifier_id = n_attrs.get("label_field_name") or match_ast_d(
        graph, args.n_id, "identifier"
    )
    if identifier_id:
        var_name = node_to_str(graph, identifier_id)

    value_id = n_attrs.get("label_field_value")
    return build_parameter_node(args, var_name, var_type, value_id, None)
