from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.name_equals import (
    build_name_equals_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    var_id = match_ast_d(args.ast_graph, args.n_id, "identifier")
    return build_name_equals_node(args, var_id)
