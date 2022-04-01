from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.interpolation import (
    build_interpolation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    identifier_id = match_ast_d(args.ast_graph, args.n_id, "identifier")
    return build_interpolation_node(args, identifier_id)
