from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_assignment_node(
    args: SyntaxGraphArgs,
    var_id: NId,
    val_id: NId | None,
    operator: str | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable_id=var_id,
        value_id=val_id,
        label_type="Assignment",
    )

    if operator:
        args.syntax_graph.nodes[args.n_id]["operator"] = operator

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_id)),
        label_ast="AST",
    )

    if val_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(val_id)),
            label_ast="AST",
        )

    return args.n_id
