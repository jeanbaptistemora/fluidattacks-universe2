from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.finally_clause import (
    build_finally_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block_id = match_ast_d(args.ast_graph, args.n_id, "block")
    return build_finally_clause_node(args, block_id)
