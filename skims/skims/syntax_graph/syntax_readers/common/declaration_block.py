# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
    NId,
)
from syntax_graph.syntax_nodes.declaration_block import (
    build_declaration_block_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, *c_ids, _ = adj_ast(args.ast_graph, args.n_id)  # do not consider { }

    ignored_labels = set()
    if args.language == GraphLanguage.CSHARP:
        ignored_labels = {"preprocessor_call"}

    filtered_ids = (
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_labels
    )
    return build_declaration_block_node(
        args, cast(Iterator[str], filtered_ids)
    )
