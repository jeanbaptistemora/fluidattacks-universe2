# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
        "decimal_integer_literal",
        "interpreted_string_literal",
        "integral_type",
        "line_string_literal",
        "raw_string_literal",
        "predefined_type",
        "string",
        "string_literal",
        "template_string",
        "verbatim_string_literal",
    }:
        raise MissingCaseHandling(
            f"Bad string literal handling in {args.n_id}"
        )

    return build_string_literal_node(args, value=n_attrs["label_text"])
