from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parenthesized_expression import (
    build_parenthesized_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, c_id, _ = adj_ast(args.ast_graph, args.n_id)
    return build_parenthesized_expression_node(args, c_id)
