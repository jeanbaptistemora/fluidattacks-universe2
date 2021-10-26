from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> str:
    condition_id = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    true_id = args.ast_graph.nodes[args.n_id]["label_field_consequence"]
    false_id = args.ast_graph.nodes[args.n_id].get("label_field_alternative")
    return build_if_node(args, condition_id, true_id, false_id)
