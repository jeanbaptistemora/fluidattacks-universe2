from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    List,
    Optional,
)


def build_property_declaration_node(
    args: SyntaxGraphArgs,
    var_type: Optional[str],
    identifier: Optional[str],
    accessors: List[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        predefined_type=var_type,
        label_type="PropertyDeclaration",
        identifier=identifier,
    )
    for node in accessors:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(node)),
            label_ast="AST",
        )

    return args.n_id
