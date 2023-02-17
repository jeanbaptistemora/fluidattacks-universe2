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
    as_attrs = args.ast_graph.nodes[args.n_id]
    var_id = as_attrs["label_field_target"]
    val_id = as_attrs.get("label_field_result")
    operator = as_attrs.get("label_field_operator")
    return build_assignment_node(args, var_id, val_id, operator)
