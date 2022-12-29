from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.while_statement import (
    build_while_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    match_childs = match_ast(graph, args.n_id, "block", "binary_expression")

    block_id = match_childs.get("block")
    if not block_id:
        raise MissingCaseHandling(
            f"Bad while statement handling in {args.n_id}"
        )

    if graph.nodes[block_id]["label_type"] == "expression_statement":
        block_id = str(adj_ast(graph, block_id)[0])

    conditional_node = match_childs.get("binary_expression")

    return build_while_statement_node(args, block_id, conditional_node)
