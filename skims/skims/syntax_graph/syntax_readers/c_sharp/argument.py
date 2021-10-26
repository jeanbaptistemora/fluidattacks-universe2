from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> str:
    first_child, *other_childs = adj_ast(args.ast_graph, args.n_id)

    if other_childs:
        raise MissingCaseHandling(f"Bad argument handling in {args.n_id}")
    return args.generic(args.fork_n_id(first_child))
