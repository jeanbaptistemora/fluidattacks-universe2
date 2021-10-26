from syntax_graph.syntax_nodes.throw import (
    build_throw_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> str:
    match = match_ast(args.ast_graph, args.n_id, "throw", ";")
    return build_throw_node(args, expression_id=match["__0__"])
