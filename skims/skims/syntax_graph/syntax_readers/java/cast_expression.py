from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.cast_expression import (
    build_cast_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]

    type_id = n_attrs["label_field_type"]
    cast_type = node_to_str(args.ast_graph, type_id)

    val_id = n_attrs["label_field_value"]

    return build_cast_expression_node(args, cast_type, val_id)
