from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    expr_id = match_ast_d(args.ast_graph, args.n_id, "lambda_expression")
    if expr_id:
        return args.generic(args.fork_n_id(expr_id))

    raise MissingCaseHandling(
        f"Bad function declaration handling in {args.n_id}"
    )
