from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.initializer_expression import (
    build_initializer_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = match_ast_group_d(
        args.ast_graph, args.n_id, "assignment_expression"
    )
    return build_initializer_expression_node(args, iter(c_ids))
