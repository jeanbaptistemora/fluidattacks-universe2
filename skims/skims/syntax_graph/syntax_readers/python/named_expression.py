from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    var_id = n_attrs["label_field_name"]
    val_id = n_attrs["label_field_value"]
    return build_assignment_node(args, var_id, val_id, None)
