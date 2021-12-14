from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_import_statement_node(args: SyntaxGraphArgs, expression: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expression,
        label_type="Import",
    )

    return args.n_id
