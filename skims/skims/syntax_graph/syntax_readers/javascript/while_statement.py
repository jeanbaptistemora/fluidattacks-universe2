from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.while_statement import (
    build_while_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "parenthesized_expression",
        "statement_block",
    )
    block_node = str(match_childs["statement_block"])
    conditional_node = str(match_childs["parenthesized_expression"])

    return build_while_statement_node(args, block_node, conditional_node)
