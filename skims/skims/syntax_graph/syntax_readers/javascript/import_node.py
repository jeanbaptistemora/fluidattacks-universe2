from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression="import",
        label_type="Import",
    )

    return args.n_id
