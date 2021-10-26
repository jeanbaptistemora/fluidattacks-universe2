from syntax_graph.syntax_nodes.file import (
    build_file_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> str:
    return build_file_node(args, c_ids=adj_ast(args.ast_graph, args.n_id))
