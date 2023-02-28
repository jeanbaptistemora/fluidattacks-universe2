from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    attrs = args.ast_graph.nodes[args.n_id]
    var_id = attrs["label_field_name"]
    if graph.nodes[var_id]["label_type"] == "pattern":
        identifier = graph.nodes[var_id]["label_field_bound_identifier"]
        var_id = node_to_str(graph, identifier)
    val_id = attrs.get("label_field_value")
    return build_variable_declaration_node(args, var_id, None, val_id)
