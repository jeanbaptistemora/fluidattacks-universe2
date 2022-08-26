from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.dimensions_expr import (
    build_dimensions_expr_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(args.ast_graph, args.n_id, "[", "]")
    expr_type = children.get("__0__")
    return build_dimensions_expr_node(args, expr_type)
