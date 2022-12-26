from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.finally_clause import (
    build_finally_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block = graph.nodes[args.n_id].get("label_field_block_statements")
    return build_finally_clause_node(args, block)
