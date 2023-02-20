from collections.abc import (
    Iterable,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_modifiers_node(
    args: SyntaxGraphArgs, annotation_ids: Iterable[str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Modifiers",
    )

    for at_id in annotation_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(at_id)),
            label_ast="AST",
        )

    return args.n_id
