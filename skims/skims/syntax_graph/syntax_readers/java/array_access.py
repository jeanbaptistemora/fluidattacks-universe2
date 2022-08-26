from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_access import (
    build_array_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_id = args.ast_graph.nodes[args.n_id]
    index = args.ast_graph.nodes[node_id["label_field_index"]]["label_text"]
    array_id = node_id["label_field_array"]
    return build_array_access_node(args, index, array_id)
