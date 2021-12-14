from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, ";")

    if len(match) == 2 and match[";"]:
        expression_id = match["__0__"]
        return args.generic(args.fork_n_id(expression_id))

    raise MissingCaseHandling(f"Bad expression handling in {args.n_id}")
