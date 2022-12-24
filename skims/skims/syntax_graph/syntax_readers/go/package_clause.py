from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.package_declaration import (
    build_package_declaration_node,
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
    childs = match_ast(args.ast_graph, args.n_id)
    if c_id := childs.get("__1__"):
        expression = node_to_str(args.ast_graph, c_id)
    else:
        expression = "packageimport"
    return build_package_declaration_node(args, expression)
