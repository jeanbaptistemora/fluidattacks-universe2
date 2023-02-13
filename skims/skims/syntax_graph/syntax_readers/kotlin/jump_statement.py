from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.return_statment import (
    build_return_node,
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
    match = match_ast(args.ast_graph, args.n_id, "throw", "return")
    val_id = match.get("__0__")
    if match.get("throw") and val_id:
        return build_throw_node(args, val_id)
    if match.get("return") and val_id:
        return build_return_node(args, val_id)

    return build_return_node(args, None)
