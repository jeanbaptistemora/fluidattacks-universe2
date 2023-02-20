from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.try_statement import (
    build_try_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    try_node = args.ast_graph.nodes[args.n_id]
    block_id = try_node["label_field_body"]
    handler_id = try_node.get("label_field_handler")
    finalizer_id = try_node.get("label_field_finalizer")
    catch_clauses: list[NId] = []
    if finalizer_id:
        catch_clauses.append(finalizer_id)

    return build_try_statement_node(
        args, block_id, catch_clauses, handler_id, None
    )
