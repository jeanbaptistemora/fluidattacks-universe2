from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
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
    n_attrs = graph.nodes[args.n_id]
    value_id = n_attrs.get("label_field_value")
    if not value_id:
        value_id = adj_ast(graph, args.n_id)[-1]

    identifier_id = n_attrs.get("label_field_name")
    if identifier_id:
        arg_name = node_to_str(graph, identifier_id)
        return build_named_argument_node(args, None, value_id, arg_name)

    return args.generic(args.fork_n_id(str(value_id)))
