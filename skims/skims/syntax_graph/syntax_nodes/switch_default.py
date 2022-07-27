from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_switch_default_node(args: SyntaxGraphArgs, expression: NId) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchDefault",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression)),
        label_ast="AST",
    )

    return args.n_id
