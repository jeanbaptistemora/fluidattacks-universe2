from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.pair import (
    build_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    key_id = n_attrs["label_field_key"]
    value_id = n_attrs["label_field_value"]
    if args.ast_graph.nodes[value_id]["label_type"] == "block_node":
        value_id = adj_ast(args.ast_graph, value_id)[-1]

    return build_pair_node(args, key_id, value_id)
