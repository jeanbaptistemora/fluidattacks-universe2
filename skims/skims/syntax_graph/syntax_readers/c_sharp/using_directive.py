from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(
        args.ast_graph, args.n_id, "using", ";", "qualified_name"
    )
    expression = "UsingDirective"
    if len(match) >= 3 and match["using"] and match[";"]:
        expression_id = match["qualified_name"] or match["__0__"]
        expression = node_to_str(args.ast_graph, str(expression_id))

    node_attrs: dict[str, str] = {
        "expression": expression,
    }
    return build_import_statement_node(args, node_attrs)
