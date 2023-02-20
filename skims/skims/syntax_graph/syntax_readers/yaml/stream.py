from collections.abc import (
    Iterator,
)
from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.file import (
    build_file_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    ignored_labels = {
        "---",
    }
    body_id = match_ast_d(args.ast_graph, args.n_id, "document")
    block_id = match_ast_d(args.ast_graph, str(body_id), "block_node")
    if block_id:
        c_ids = adj_ast(args.ast_graph, block_id)
        filtered_ids = (
            _id
            for _id in c_ids
            if args.ast_graph.nodes[_id]["label_type"] not in ignored_labels
        )
        return build_file_node(args, cast(Iterator[str], filtered_ids))

    return str(body_id)
