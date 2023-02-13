from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    class_node = graph.nodes[args.n_id]

    name = "AnonymousClass"
    name_id = class_node.get("label_field_identifier")
    if name_id:
        name = node_to_str(graph, name_id)

    block_id = class_node.get("label_field_class_body")
    if not block_id:
        block_id = str(adj_ast(graph, args.n_id)[-1])

    return build_class_node(args, name, block_id, None)
