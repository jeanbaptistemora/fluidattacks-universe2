from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> str:
    match = match_ast(args.ast_graph, args.n_id, "using", ";")

    if len(match) == 3 and match["using"] and match[";"]:
        expression_id = match["__0__"]
        expression = node_to_str(args.ast_graph, expression_id)
        return build_import_statement_node(args, expression)

    raise MissingCaseHandling(f"Bad using handling in {args.n_id}")
