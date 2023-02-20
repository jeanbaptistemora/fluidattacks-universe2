from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_resource_node(
    args: SyntaxGraphArgs,
    variable: str,
    variable_type: str | None,
    value: str | None,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        variable=variable,
        variable_type=variable_type,
        value_id=value,
        label_type="Resource",
    )

    if value:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value)),
            label_ast="AST",
        )

    return args.n_id
