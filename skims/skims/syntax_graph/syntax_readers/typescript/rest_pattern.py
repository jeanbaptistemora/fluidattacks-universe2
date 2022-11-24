from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "...")
    identifier_id = match["__0__"]

    return args.generic(args.fork_n_id(str(identifier_id)))
