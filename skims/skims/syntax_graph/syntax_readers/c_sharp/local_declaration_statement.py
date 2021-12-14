from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    decl_id = match_ast_d(args.ast_graph, args.n_id, "variable_declaration")
    return args.generic(args.fork_n_id(decl_id))
