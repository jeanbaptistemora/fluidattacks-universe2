from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_extension_declaration_node(
    args: SyntaxGraphArgs,
    class_id: NId,
    body_id: NId,
    extension_name: Optional[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        class_id=class_id,
        body_id=body_id,
        label_type="ExtensionDeclaration",
    )

    if extension_name:
        args.syntax_graph.nodes[args.n_id]["name"] = extension_name

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(class_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_id)),
        label_ast="AST",
    )

    return args.n_id
