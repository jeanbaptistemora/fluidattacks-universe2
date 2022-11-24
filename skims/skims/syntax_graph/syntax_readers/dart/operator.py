from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.operator import (
    build_operator_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = args.ast_graph.nodes[args.n_id]
    val_str = n_attrs.get("label_text") or node_to_str(graph, args.n_id)
    return build_operator_node(args, value=val_str)
