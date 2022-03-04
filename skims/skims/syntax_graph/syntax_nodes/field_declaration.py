from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_field_declaration_node(
    args: SyntaxGraphArgs,
    var: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id, label_type="FieldDeclaration", variable_id=var
    )
    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var)),
        label_ast="AST",
    )

    return args.n_id
