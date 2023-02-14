from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.using_statement import (
    build_using_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block_id = graph.nodes[args.n_id]["label_field_body"]
    if graph.nodes[block_id]["label_type"] == "expression_statement":
        block_id = adj_ast(graph, block_id)[0]

    with_clause = match_ast_d(graph, args.n_id, "with_clause")
    if with_clause:
        with_item = match_ast_d(graph, with_clause, "with_item")
        if with_item:
            with_clause = adj_ast(graph, with_item)[0]

    return build_using_statement_node(args, block_id, with_clause)
