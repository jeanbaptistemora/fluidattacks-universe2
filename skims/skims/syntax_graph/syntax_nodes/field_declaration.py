from collections.abc import (
    Iterable,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_field_declaration_node(
    args: SyntaxGraphArgs, vars_list: Iterable[str], field_type: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        field_type=field_type,
        label_type="FieldDeclaration",
    )

    for var_id in vars_list:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(var_id)),
            label_ast="AST",
        )

    return args.n_id
