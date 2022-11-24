from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
    Optional,
)


def build_parameter_node(
    args: SyntaxGraphArgs,
    variable: Optional[str],
    variable_type: Optional[str],
    value_id: Optional[NId],
    c_ids: Optional[Iterator[NId]] = None,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="Parameter",
    )

    if variable:
        args.syntax_graph.nodes[args.n_id]["variable"] = variable

    if variable_type:
        args.syntax_graph.nodes[args.n_id]["variable_type"] = variable_type

    if value_id:
        args.syntax_graph.nodes[args.n_id]["value_id"] = value_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(value_id)),
            label_ast="AST",
        )

    if c_ids:
        for c_id in c_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(c_id)),
                label_ast="AST",
            )

    return args.n_id
