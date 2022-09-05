from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.do_statement import (
    build_do_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "block",
        "statement_block",
        "while",
        "binary_expression",
        "parenthesized_expression",
    )

    if match_childs.get("block"):
        block_node = str(match_childs["block"])
    else:
        block_node = str(match_childs["statement_block"])

    if match_childs.get("binary_expression"):
        conditional_node = str(match_childs["binary_expression"])
    elif match_childs.get("while"):
        conditional_node = str(match_childs["parenthesized_expression"])
    else:
        raise MissingCaseHandling(f"Bad do statement handling in {args.n_id}")

    return build_do_statement_node(args, block_node, conditional_node)
