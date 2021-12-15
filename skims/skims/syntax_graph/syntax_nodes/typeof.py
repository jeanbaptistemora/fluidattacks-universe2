from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_typeof_node(args: SyntaxGraphArgs, argument_id: NId) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        argument_id=argument_id,
        label_type="TypeOf",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(argument_id)),
        label_ast="AST",
    )

    return args.n_id
