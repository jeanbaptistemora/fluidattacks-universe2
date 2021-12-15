from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.bool_literal import (
    build_bool_literal_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    node_type = n_attrs["label_type"]

    if node_type not in {"false", "true", "boolean_literal"}:
        raise MissingCaseHandling(f"Bad bool literal handling in {args.n_id}")

    return build_bool_literal_node(args, value=n_attrs["label_text"])
