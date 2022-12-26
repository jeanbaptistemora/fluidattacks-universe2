from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.try_statement import (
    build_try_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    block_id = graph.nodes[args.n_id].get("label_field_block_statements")
    if not block_id:
        raise MissingCaseHandling(f"Bad try statement handling in {args.n_id}")

    catch_blocks = match_ast_group_d(args.ast_graph, args.n_id, "catch_block")
    finally_block = graph.nodes[args.n_id].get("label_field_finally_block")

    return build_try_statement_node(
        args, block_id, catch_blocks, finally_block, None
    )
