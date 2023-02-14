from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_each_statement import (
    build_for_each_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    node = graph.nodes[args.n_id]
    var_node = node.get("label_field_left")
    iterable_item = node.get("label_field_right")

    return build_for_each_statement_node(args, var_node, iterable_item, None)
