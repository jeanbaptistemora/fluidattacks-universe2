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
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    if (
        block_id := n_attrs.get("label_field_block_statements")
    ) and graph.nodes[block_id]["label_type"] == "statements":
        c_ids = adj_ast(graph, block_id)
    else:
        childs = adj_ast(graph, args.n_id)
        if len(childs) > 2:
            c_ids = childs[1:-1]  # ignore { }
        else:
            c_ids = childs
    return build_execution_block_node(args, cast(Iterator[NId], c_ids))
