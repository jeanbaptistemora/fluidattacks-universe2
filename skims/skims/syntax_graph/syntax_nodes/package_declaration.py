from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_package_declaration_node(
    args: SyntaxGraphArgs, p_id: Optional[str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        package_identifier=p_id,
        label_type="PackageDeclaration",
    )

    return args.n_id
