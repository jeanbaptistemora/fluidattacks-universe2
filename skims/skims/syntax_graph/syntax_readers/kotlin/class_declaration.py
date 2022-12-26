from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    class_node = args.ast_graph.nodes[args.n_id]

    name = "AnonymousClass"
    name_id = class_node.get("label_field_identifier")
    if name_id:
        name = node_to_str(args.ast_graph, name_id)

    block_id = class_node.get("label_field_class_body")
    if not block_id:
        raise MissingCaseHandling(
            f"Bad class Declaration handling in {args.n_id}"
        )

    return build_class_node(args, name, block_id, None)
