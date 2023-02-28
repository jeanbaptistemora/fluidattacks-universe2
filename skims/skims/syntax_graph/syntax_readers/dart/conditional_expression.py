from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
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

    if not conditional_node:
        raise MissingCaseHandling(
            f"Bad conditional expression handling in {args.n_id}"
        )

    return build_if_node(args, conditional_node, true_block, false_block)
