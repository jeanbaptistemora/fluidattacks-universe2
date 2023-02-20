from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_catch_parameter_node(
    args: SyntaxGraphArgs,
    variable: str,
    catch_type: NId | None,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        variable_name=variable,
        label_type="CatchParameter",
    )
    if catch_type:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(catch_type)),
            label_ast="AST",
        )

    return args.n_id
