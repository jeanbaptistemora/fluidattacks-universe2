# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.pair import (
    build_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    key_id = args.ast_graph.nodes[args.n_id]["label_field_key"]
    value_id = args.ast_graph.nodes[args.n_id]["label_field_value"]

    return build_pair_node(args, key_id, value_id)
