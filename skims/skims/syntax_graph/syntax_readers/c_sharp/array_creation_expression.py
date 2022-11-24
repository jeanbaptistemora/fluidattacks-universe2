from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_creation_expression import (
    build_array_creation_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(
        args.ast_graph, args.n_id, "array_type", "initializer_expression"
    )
    type_id = children.get("array_type")
    if type_id:
        arr_type = node_to_str(args.ast_graph, type_id)
    else:
        arr_type = "Undefined"

    arr_init = children.get("initializer_expression")

    return build_array_creation_expression_node(args, arr_type, arr_init)
