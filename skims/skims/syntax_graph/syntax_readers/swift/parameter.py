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
    attrs = args.ast_graph.nodes[args.n_id]

    var_id = attrs["label_field_name"]
    var_name = node_to_str(args.ast_graph, var_id)

    var_type = attrs.get("label_field_type")

    return build_parameter_node(args, var_name, var_type, None)
