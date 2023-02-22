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
    expr_id = match_ast_d(args.ast_graph, args.n_id, "integer_literal")

    if not expr_id:
        expr_id = match_ast_d(args.ast_graph, args.n_id, "simple_identifier")

    if not expr_id:
        raise MissingCaseHandling(
            f"Bad navigation suffix handling in {args.n_id}"
        )

    return args.generic(args.fork_n_id(str(expr_id)))
