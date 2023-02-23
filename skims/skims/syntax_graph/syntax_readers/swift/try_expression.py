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


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    block_id = graph.nodes[args.n_id].get("label_field_expr")
    if not block_id:
        raise MissingCaseHandling(f"Bad try statement handling in {args.n_id}")

    return build_try_statement_node(args, block_id, None, None, None)
