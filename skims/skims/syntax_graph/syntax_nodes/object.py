from collections.abc import (
    Iterator,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_object_node(
    args: SyntaxGraphArgs,
    c_ids: Iterator[NId],
    name: str | None = None,
    tf_reference: str | None = None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Object",
    )

    if name:
        args.syntax_graph.nodes[args.n_id]["name"] = name

    if tf_reference:
        args.syntax_graph.nodes[args.n_id]["tf_reference"] = tf_reference

    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
