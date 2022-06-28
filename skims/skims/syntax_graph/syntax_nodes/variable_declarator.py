from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_variable_declarator_node(
    args: SyntaxGraphArgs, ident_id: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        identifier_id=ident_id,
        label_type="VariableDeclarator",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(ident_id)),
        label_ast="AST",
    )

    return args.n_id
