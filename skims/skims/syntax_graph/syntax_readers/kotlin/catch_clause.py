from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.catch_clause import (
    build_catch_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block = graph.nodes[args.n_id]["label_field_block_statements"]
    parameter = graph.nodes[args.n_id].get("label_field_identifier")
    return build_catch_clause_node(args, block, None, None, parameter)
