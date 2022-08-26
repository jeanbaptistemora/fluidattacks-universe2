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


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(
        args.ast_graph, args.n_id, "integral_type", "dimensions_expr"
    )
    arr_type = children.get("integral_type")
    arr_init = children.get("dimensions_expr")
    return build_array_creation_expression_node(args, arr_type, arr_init)
