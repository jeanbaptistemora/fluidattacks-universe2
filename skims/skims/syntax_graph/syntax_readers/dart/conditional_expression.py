from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.conditional_expression import (
    build_conditional_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:

    conditional_node = None

    invalid_types = {
        "?",
        ":",
    }

    true_block = args.ast_graph.nodes[args.n_id]["label_field_consequence"]
    false_block = args.ast_graph.nodes[args.n_id]["label_field_alternative"]

    reserved_ids = {
        true_block,
        false_block,
    }

    frst_child = match_ast(args.ast_graph, args.n_id).get("__0__")
    if (
        frst_child
        and args.ast_graph.nodes[frst_child]["label_type"] not in invalid_types
        and frst_child not in reserved_ids
    ):
        conditional_node = frst_child

    return build_conditional_expression_node(
        args, conditional_node, true_block, false_block
    )
