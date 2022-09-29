# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.reserved_word import (
    build_reserved_word_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    node_type = n_attrs["label_type"]

    if node_type not in {
        "get",
        "inferred_type",
        "this",
    }:
        raise MissingCaseHandling(f"Bad reserved word handling in {args.n_id}")

    return build_reserved_word_node(
        args, node_to_str(args.ast_graph, args.n_id)
    )
