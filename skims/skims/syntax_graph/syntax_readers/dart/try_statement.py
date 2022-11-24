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
    match_ast_d,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    try_node = graph.nodes[args.n_id]
    block_id = try_node["label_field_body"]

    catch_clauses = match_ast_group_d(graph, args.n_id, "block")
    if len(catch_clauses) > 0 and catch_clauses[0] == block_id:
        catch_clauses.pop(0)

    if finally_clause := match_ast_d(graph, args.n_id, "finally_clause"):
        catch_clauses.append(finally_clause)

    return build_try_statement_node(args, block_id, catch_clauses, None, None)
