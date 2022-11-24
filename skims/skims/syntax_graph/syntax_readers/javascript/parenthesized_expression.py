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
    match_expression = match_ast(args.ast_graph, args.n_id)
    return args.generic(args.fork_n_id(str(match_expression["__1__"])))
