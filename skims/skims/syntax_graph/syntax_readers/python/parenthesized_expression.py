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
    childs = adj_ast(args.ast_graph, args.n_id)
    if len(childs) == 3:
        c_id = childs[1]
    else:
        c_id = childs[-2]
    return build_parenthesized_expression_node(args, c_id)
