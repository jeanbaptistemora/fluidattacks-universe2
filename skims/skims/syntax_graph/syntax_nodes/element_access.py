from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_element_access_node(
    args: SyntaxGraphArgs, expression_id: NId, arguments_id: NId
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_id=expression_id,
        arguments_id=arguments_id,
        label_type="ElementAccess",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(arguments_id)),
        label_ast="AST",
    )

    return args.n_id
