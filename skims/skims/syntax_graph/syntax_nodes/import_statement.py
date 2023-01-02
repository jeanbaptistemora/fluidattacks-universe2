from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
)


def build_import_statement_node(
    args: SyntaxGraphArgs, node_attrs: Dict[str, str]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        **node_attrs,
        label_type="Import",
    )

    return args.n_id
