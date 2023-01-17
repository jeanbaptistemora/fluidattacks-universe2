from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.file import (
    build_file_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    body_id = match_ast_d(args.ast_graph, args.n_id, "document")
    c_ids = adj_ast(args.ast_graph, str(body_id))

    return build_file_node(args, iter(c_ids))
