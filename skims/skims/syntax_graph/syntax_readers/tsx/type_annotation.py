# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.constants import (
    TSX_PRIMARY_TYPES,
)
from syntax_graph.syntax_nodes.type_annotation import (
    build_type_annotation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:

    childs_id = adj_ast(
        args.ast_graph,
        args.n_id,
    )

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] in TSX_PRIMARY_TYPES
    ]

    return build_type_annotation_node(args, valid_childs)
