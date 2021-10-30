from syntax_graph.syntax_nodes.execution_block import (
    build_execution_block_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> str:
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)  # do not consider { }
    return build_execution_block_node(args, c_ids)
