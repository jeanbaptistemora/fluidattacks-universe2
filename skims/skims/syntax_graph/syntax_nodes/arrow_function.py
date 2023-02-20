from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_arrow_function_node(
    args: SyntaxGraphArgs,
    block_id: str,
    parameters_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block_id,
        label_type="BlocklessMethodDeclaration",
    )

    if parameters_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(parameters_id)),
            label_ast="AST",
        )

    return args.n_id
