from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.element_value_pair import (
    build_element_value_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    var_id = as_attrs["label_field_key"]
    val_id = as_attrs["label_field_value"]
    return build_element_value_pair_node(args, var_id, val_id)
