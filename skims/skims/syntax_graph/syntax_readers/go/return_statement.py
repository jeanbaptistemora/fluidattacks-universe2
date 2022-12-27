from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.return_statment import (
    build_return_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "return")
    if len(match) == 2:
        return build_return_node(args, value_id=str(match["__0__"]))
    return build_return_node(args, None)
