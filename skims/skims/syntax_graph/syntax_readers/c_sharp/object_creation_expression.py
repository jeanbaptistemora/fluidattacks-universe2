from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.object_creation import (
    build_object_creation_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_attr = args.ast_graph.nodes[args.n_id]
    type_id = node_attr["label_field_type"]
    name = node_to_str(args.ast_graph, type_id)

    if arguments_id := node_attr.get("label_field_arguments"):
        if "__0__" not in match_ast(args.ast_graph, arguments_id, "(", ")"):
            arguments_id = None
        return build_object_creation_node(args, name, arguments_id)

    raise MissingCaseHandling(f"Bad object creation handling in {args.n_id}")
