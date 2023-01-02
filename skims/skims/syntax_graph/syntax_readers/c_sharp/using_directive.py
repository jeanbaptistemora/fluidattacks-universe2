from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from typing import (
    Dict,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "using", ";")

    if len(match) == 3 and match["using"] and match[";"]:
        expression_id = match["__0__"]
        expression = node_to_str(args.ast_graph, str(expression_id))
        node_attrs: Dict[str, str] = {
            "expression": expression,
        }
        return build_import_statement_node(args, node_attrs)

    raise MissingCaseHandling(f"Bad using handling in {args.n_id}")
