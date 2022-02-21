from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.execution_block import (
    build_execution_block_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)  # do not consider { }
    return build_execution_block_node(args, cast(Iterator[str], c_ids))
