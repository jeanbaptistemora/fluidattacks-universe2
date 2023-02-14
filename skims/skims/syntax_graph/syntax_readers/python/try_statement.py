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
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block_id = graph.nodes[args.n_id]["label_field_body"]
    catch_blocks = match_ast_group_d(graph, args.n_id, "except_clause")

    return build_try_statement_node(args, block_id, catch_blocks, None, None)
