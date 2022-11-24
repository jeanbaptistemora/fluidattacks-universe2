from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.instanceof_expression import (
    build_instanceof_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    field_left = as_attrs["label_field_left"]
    field_right = as_attrs["label_field_right"]

    return build_instanceof_expression_node(
        args,
        field_left,
        field_right,
    )
