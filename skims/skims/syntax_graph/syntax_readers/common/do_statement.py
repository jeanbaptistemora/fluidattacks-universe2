from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph, args.n_id, "block", "binary_expression"
    )
    block_node = match_childs["block"]
    conditional_node = match_childs["binary_expression"]
    return build_do_statement_node(args, block_node, conditional_node)
