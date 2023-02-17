from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    attrs = args.ast_graph.nodes[args.n_id]
    var_id = attrs["label_field_name"]
    val_id = attrs.get("label_field_value")
    return build_variable_declaration_node(args, var_id, None, val_id)
