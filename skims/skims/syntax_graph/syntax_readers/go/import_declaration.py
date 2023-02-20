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
    childs_id = match_ast(args.ast_graph, args.n_id)
    if childs_id["__1__"]:
        import_text = node_to_str(args.ast_graph, childs_id["__1__"])
    else:
        import_text = node_to_str(args.ast_graph, args.n_id)

    node_attrs: dict[str, str] = {
        "expression": import_text,
    }
    return build_import_statement_node(args, node_attrs)
