from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.while_statement import (
    build_while_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block = graph.nodes[args.n_id]["label_field_block_statements"]
    conditional_node = graph.nodes[args.n_id].get("label_field_condition")

    return build_while_statement_node(args, block, conditional_node)
