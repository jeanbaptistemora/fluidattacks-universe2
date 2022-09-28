# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.comment import (
    build_comment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    comment = (
        comment_text
        if (comment_text := args.ast_graph.nodes[args.n_id].get("label_text"))
        else node_to_str(args.ast_graph, args.n_id)
    )

    return build_comment_node(args, comment)
