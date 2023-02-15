from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.conditional_access_expression import (
    build_conditional_access_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    binding = adj_ast(args.ast_graph, args.n_id)[-1]
    return build_conditional_access_expression_node(args, "IfClause", binding)
