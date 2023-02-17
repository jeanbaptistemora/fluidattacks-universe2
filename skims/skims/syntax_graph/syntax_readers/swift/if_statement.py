from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:

    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]

    condition_id = n_attrs.get("label_field_condition")

    if not condition_id and (
        ident := match_ast_d(graph, args.n_id, "simple_identifier")
    ):
        condition_id = ident

    if not condition_id:
        raise MissingCaseHandling(f"Bad if statement handling in {args.n_id}")

    statements = match_ast_group_d(graph, args.n_id, "statements")

    true_id = None
    false_id = None

    if len(statements) == 2:
        true_id = statements[0]
        false_id = statements[1]
    elif len(statements) == 1:
        true_id = statements[0]

    if false_statement := match_ast_d(graph, args.n_id, "if_statement"):
        false_id = false_statement

    return build_if_node(args, condition_id, true_id, false_id)
