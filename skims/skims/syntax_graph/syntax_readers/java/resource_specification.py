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
    resource_id = match_ast_d(args.ast_graph, args.n_id, "resource")
    if not resource_id:
        raise MissingCaseHandling(f"Bad resource specification in {args.n_id}")
    return args.generic(args.fork_n_id(resource_id))
