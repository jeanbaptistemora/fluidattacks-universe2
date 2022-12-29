from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.for_each_statement import (
    build_for_each_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    node = graph.nodes[args.n_id]
    var_node = node.get("label_field_left")
    iterable_item = node.get("label_field_right")
    block_id = node.get("label_field_body")

    if not (var_node and iterable_item and block_id):
        raise MissingCaseHandling(f"Bad for statement handling in {args.n_id}")

    if graph.nodes[block_id]["label_type"] == "expression_statement":
        block_id = match_ast(graph, block_id)["__0__"]

    return build_for_each_statement_node(
        args, var_node, iterable_item, block_id
    )
