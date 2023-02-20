from collections.abc import (
    Iterable,
)
from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_switch_body_node(
    args: SyntaxGraphArgs,
    case_ids: Iterable[NId],
    default_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchBody",
    )

    for c_id in case_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    if default_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(default_id)),
            label_ast="AST",
        )

    return args.n_id
