from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.statement_block import (
    build_statement_block_node,
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
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)
    ignored_labels = {
        "\n",
        "\r\n",
    }
    filtered_ids = (
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_labels
    )
    return build_statement_block_node(args, cast(Iterator[str], filtered_ids))
