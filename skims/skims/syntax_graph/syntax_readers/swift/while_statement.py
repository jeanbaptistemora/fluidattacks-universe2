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
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    condition_id = n_attrs["label_field_condition"]
    block = match_ast_d(graph, args.n_id, "statements")

    if not block:
        raise MissingCaseHandling(
            f"Bad while statement handling in {args.n_id}"
        )

    return build_while_statement_node(args, block, condition_id)
