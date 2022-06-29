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
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    p_id = match_ast_d(args.ast_graph, args.n_id, "scoped_identifier")
    return build_package_declaration_node(args, p_id)
