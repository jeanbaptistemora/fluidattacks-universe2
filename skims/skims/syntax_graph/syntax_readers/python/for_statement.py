from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_statement import (
    build_for_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]
    var_node = n_attrs["label_field_left"]
    condition_node = n_attrs["label_field_right"]

    return build_for_statement_node(
        args, var_node, condition_node, None, body_id
    )
