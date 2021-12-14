from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    node_type = n_attrs["label_type"]

    if node_type not in {
        "character_literal",
        "interpreted_string_literal",
        "line_string_literal",
        "raw_string_literal",
        "string_literal",
        "verbatim_string_literal",
        "string",
    }:
        raise MissingCaseHandling(
            f"Bad string literal handling in {args.n_id}"
        )

    value = n_attrs["label_text"][1:-1]  # remove " "
    return build_string_literal_node(args, str(value))
