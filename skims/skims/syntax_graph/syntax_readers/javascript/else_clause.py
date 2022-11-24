from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.else_clause import (
    build_else_clause_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    match = match_ast(graph, args.n_id, "else")
    body_id = match.get("__0__")

    if (
        body_id
        and graph.nodes[body_id]["label_type"] == "expression_statement"
    ):
        body_id = match_ast(graph, body_id).get("__0__")

    if (
        body_id
        and graph.nodes[body_id]["label_type"] == "parenthesized_expression"
    ):
        body_id = match_ast(graph, body_id).get("__1__")

    if not body_id:
        raise MissingCaseHandling(f"Bad else handling in {args.n_id}")

    return build_else_clause_node(args, body_id)
