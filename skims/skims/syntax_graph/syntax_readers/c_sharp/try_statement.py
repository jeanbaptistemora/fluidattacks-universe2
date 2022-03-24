from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.try_statement import (
    build_try_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block_node = args.ast_graph.nodes[args.n_id]["label_field_body"]
    childs = match_ast(
        args.ast_graph, args.n_id, "catch_clause", "finally_clause"
    )
    catch_block = childs.get("catch_clause")
    try_block = childs.get("finally_clause")

    return build_try_statement_node(args, block_node, catch_block, try_block)
