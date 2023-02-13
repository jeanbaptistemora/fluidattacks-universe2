from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    for child in c_ids:
        return args.generic(args.fork_n_id(child))

    raise MissingCaseHandling(f"Bad expression handling in {args.n_id}")
