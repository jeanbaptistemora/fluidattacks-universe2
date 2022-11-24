from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.arrow_expression_clause import (
    build_arrow_expression_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, block_node = adj_ast(args.ast_graph, args.n_id)
    return build_arrow_expression_clause_node(args, block_node)
