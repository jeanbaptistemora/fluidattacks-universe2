from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
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
    n_attrs = graph.nodes[args.n_id]
    var_id = n_attrs["label_field_left"]
    val_id = n_attrs.get("label_field_right")
    type_id = n_attrs.get("label_field_type")
    if graph.nodes[var_id]["label_type"] == "identifier":
        var_name = node_to_str(graph, n_attrs["label_field_left"])
        var_type = None
        if type_id:
            var_type = node_to_str(graph, type_id)
        return build_variable_declaration_node(
            args, var_name, var_type, val_id
        )

    return build_assignment_node(args, var_id, val_id, type_id)
