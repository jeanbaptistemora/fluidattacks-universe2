from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_parameter_node(
    args: SyntaxGraphArgs, variable: str, variable_type: Optional[str]
) -> str:

    args.syntax_graph.add_node(
        args.n_id,
        variable=variable,
        variable_type=variable_type,
        danger=False,
        label_type="Parameter",
    )

    return args.n_id
