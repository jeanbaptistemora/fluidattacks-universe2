from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_update_expression_node(
    args: SyntaxGraphArgs, expression_type: str, identifier_id: NId | None
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_type=expression_type,
        label_type="UpdateExpression",
    )

    if identifier_id:
        args.syntax_graph.nodes[args.n_id]["identifier_id"] = identifier_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(identifier_id)),
            label_ast="AST",
        )

    return args.n_id
