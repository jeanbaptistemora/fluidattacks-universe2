from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parenthesized_expression import (
    build_parenthesized_expression_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    expr_id = match_ast(args.ast_graph, args.n_id).get("__1__")
    if not expr_id:
        raise MissingCaseHandling(
            f"Bad parenthesized expression in {args.n_id}"
        )
    return build_parenthesized_expression_node(args, expr_id)
