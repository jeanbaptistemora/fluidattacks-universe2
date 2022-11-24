from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.global_statement import (
    build_global_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    return build_global_statement_node(args, iter(c_ids))
