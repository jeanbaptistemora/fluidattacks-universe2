from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.literal import (
    build_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    value_id = n_attrs["label_field_operand"]
    value = node_to_str(args.ast_graph, value_id)
    type_id = n_attrs["label_field_type"]
    var_type = node_to_str(args.ast_graph, type_id)
    return build_literal_node(args, value, var_type)
