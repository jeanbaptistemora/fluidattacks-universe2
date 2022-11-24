from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.namespace import (
    build_namespace_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    namespace = args.ast_graph.nodes[args.n_id]
    block_id = namespace["label_field_body"]
    name = node_to_str(args.ast_graph, namespace["label_field_name"])
    return build_namespace_node(args, name, block_id)
