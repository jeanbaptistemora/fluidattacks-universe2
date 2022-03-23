from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.conditional_expression import (
    build_conditional_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    conditional_node = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    true_block = args.ast_graph.nodes[args.n_id]["label_field_consequence"]
    false_block = args.ast_graph.nodes[args.n_id]["label_field_alternative"]

    return build_conditional_expression_node(
        args, conditional_node, true_block, false_block
    )
