from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_annotation_node(
    args: SyntaxGraphArgs, attr_name: str, al_id: Optional[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=attr_name,
        label_type="Annotation",
    )

    if al_id:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(al_id)),
            label_ast="AST",
        )

    return args.n_id
