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
    c_types = ("identifier", "import_alias")
    childs = match_ast(args.ast_graph, args.n_id, *c_types)
    text_node = childs.get("identifier")
    if not text_node:
        raise MissingCaseHandling(
            f"Bad import expression handling in {args.n_id}"
        )
    import_text = node_to_str(args.ast_graph, text_node)
    node_attrs: Dict[str, str] = {
        "expression": import_text,
    }

    return build_import_statement_node(args, node_attrs)
