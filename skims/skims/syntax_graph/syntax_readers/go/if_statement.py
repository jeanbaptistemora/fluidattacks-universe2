from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    condition_id = n_attrs["label_field_condition"]
    true_id = n_attrs["label_field_consequence"]
    false_id = n_attrs.get("label_field_alternative")
    return build_if_node(args, condition_id, true_id, false_id)
