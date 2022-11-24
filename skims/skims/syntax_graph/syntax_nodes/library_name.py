from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_library_name_node(args: SyntaxGraphArgs, expression: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expression,
        label_type="LibraryName",
    )

    return args.n_id
