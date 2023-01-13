from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.throw import (
    build_throw_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = match_ast(args.ast_graph, args.n_id, "throw", ";")
    expr_id = childs.get("__0__")
    return build_throw_node(args, expr_id)
